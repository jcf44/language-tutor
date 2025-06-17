"""TTS client implementations for audio generation."""

import asyncio
import os
import tempfile
from abc import ABC, abstractmethod
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk
import torch
import torchaudio
from google.cloud import texttospeech
from whisperspeech.pipeline import Pipeline


class TTSClient(ABC):
    """Abstract base class for TTS clients."""

    @abstractmethod
    async def synthesize_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language_code: str = "fr-FR",
    ) -> bytes:
        """Synthesize speech from text and return audio bytes."""
        pass

    @abstractmethod
    async def get_available_voices(
        self, language_code: str = "fr-FR"
    ) -> List[str]:
        """Get list of available voices for the specified language."""
        pass


class GoogleCloudTTSClient(TTSClient):
    """Google Cloud Text-to-Speech client."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize the Google Cloud TTS client."""
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = texttospeech.TextToSpeechClient()

    async def synthesize_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language_code: str = "fr-FR",
    ) -> bytes:
        """Synthesize speech using Google Cloud TTS."""
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        if not voice_name:
            voice_name = "fr-FR-Wavenet-C"  # Default French female voice

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        try:
            # Perform the text-to-speech request
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self.client.synthesize_speech,
                {
                    "input": synthesis_input,
                    "voice": voice,
                    "audio_config": audio_config,
                },
            )

            return response.audio_content

        except Exception as e:
            raise Exception(
                f"Error synthesizing speech with Google Cloud TTS: {str(e)}"
            )

    async def get_available_voices(
        self, language_code: str = "fr-FR"
    ) -> List[str]:
        """Get available French voices from Google Cloud TTS."""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.client.list_voices, {"language_code": language_code}
            )

            voices = []
            for voice in response.voices:
                if language_code in voice.language_codes:
                    voices.append(voice.name)

            return voices

        except Exception as e:
            raise Exception(f"Error getting available voices: {str(e)}")


class AzureTTSClient(TTSClient):
    """Azure Cognitive Services Speech client."""

    def __init__(self, speech_key: str, speech_region: str):
        """Initialize the Azure TTS client."""
        self.speech_key = speech_key
        self.speech_region = speech_region
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=speech_region
        )
        self.speech_config.speech_synthesis_output_format = (
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )

    async def synthesize_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language_code: str = "fr-FR",
    ) -> bytes:
        """Synthesize speech using Azure Cognitive Services."""
        if not voice_name:
            voice_name = "fr-FR-DeniseNeural"  # Default French female voice

        self.speech_config.speech_synthesis_voice_name = voice_name

        # Create a synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

        try:
            # Perform synthesis
            result = await asyncio.get_event_loop().run_in_executor(
                None, synthesizer.speak_text, text
            )

            if (
                result.reason
                == speechsdk.ResultReason.SynthesizingAudioCompleted
            ):
                return result.audio_data
            else:
                error_msg = f"Speech synthesis failed: {result.reason}"
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = speechsdk.CancellationDetails(
                        result
                    )
                    error_msg += (
                        f" - {cancellation_details.reason}: "
                        f"{cancellation_details.error_details}"
                    )
                raise Exception(error_msg)

        except Exception as e:
            raise Exception(
                f"Error synthesizing speech with Azure TTS: {str(e)}"
            )

    async def get_available_voices(
        self, language_code: str = "fr-FR"
    ) -> List[str]:
        """Get available French voices from Azure TTS."""
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=None
        )

        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None, synthesizer.get_voices_async().get
            )

            voices = []
            for voice in result.voices:
                if language_code.lower() in voice.locale.lower():
                    voices.append(voice.short_name)

            return voices

        except Exception as e:
            raise Exception(f"Error getting available voices: {str(e)}")


class WhisperSpeechTTSClient(TTSClient):
    """WhisperSpeech TTS client for high-quality open-source TTS."""

    def __init__(self):
        """Initialize the WhisperSpeech TTS client."""
        self.pipeline = None
        self.sample_rate = 24000  # WhisperSpeech default sample rate

    def _get_pipeline(self):
        """Lazy initialization of WhisperSpeech pipeline."""
        if self.pipeline is None:
            # Initialize with a small, efficient model
            self.pipeline = Pipeline(
                s2a_ref="collabora/whisperspeech:s2a-q4-tiny-en+pl.model"
            )
        return self.pipeline

    async def synthesize_speech(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language_code: str = "fr-FR",
    ) -> bytes:
        """Synthesize speech using WhisperSpeech."""
        try:
            # Get pipeline
            pipeline = self._get_pipeline()

            # Generate audio
            audio_tensor = await asyncio.get_event_loop().run_in_executor(
                None, pipeline.generate, text
            )

            # Convert to bytes (WAV format)
            # Create a temporary file to save the audio
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False
            ) as tmp_file:
                # Save as WAV file
                torchaudio.save(
                    tmp_file.name, audio_tensor.unsqueeze(0), self.sample_rate
                )

                # Read the file back as bytes
                with open(tmp_file.name, "rb") as f:
                    audio_bytes = f.read()

                # Clean up temporary file
                os.unlink(tmp_file.name)

                return audio_bytes

        except Exception as e:
            raise Exception(
                f"Error synthesizing speech with WhisperSpeech: {str(e)}"
            )

    async def get_available_voices(
        self, language_code: str = "fr-FR"
    ) -> List[str]:
        """Get available voices for WhisperSpeech."""
        # WhisperSpeech supports voice cloning but doesn't have
        # predefined voice names like cloud services
        # For now, return a default voice identifier
        return ["whisperspeech-default"]


async def save_audio_file(audio_data: bytes, filename: str) -> str:
    """Save audio data to a file and return the file path."""
    try:
        # Create output directory if it doesn't exist
        output_dir = "audio_output"
        os.makedirs(output_dir, exist_ok=True)

        # Create full file path
        file_path = os.path.join(output_dir, filename)

        # Write audio data to file
        with open(file_path, "wb") as f:
            f.write(audio_data)

        return file_path

    except Exception as e:
        raise Exception(f"Error saving audio file: {str(e)}")


async def create_temp_audio_file(audio_data: bytes) -> str:
    """Create a temporary audio file and return its path."""
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as tmp_file:
            tmp_file.write(audio_data)
            return tmp_file.name

    except Exception as e:
        raise Exception(f"Error creating temporary audio file: {str(e)}")
