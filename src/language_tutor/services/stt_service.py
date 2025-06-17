"""Service for handling speech-to-text (STT) functionality."""

import asyncio
from typing import Any, Dict, Optional

import speech_recognition as sr

from ..models.config import AppConfig


class STTService:
    """Service for speech-to-text conversion."""

    def __init__(self, config: AppConfig):
        """Initialize the STT service with configuration."""
        self.config = config
        self.recognizer = sr.Recognizer()

    def _calibrate_microphone(self, microphone):
        """Calibrate microphone for ambient noise."""
        try:
            with microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Warning: Could not calibrate microphone: {str(e)}")

    async def listen_for_speech(
        self,
        timeout: int = 5,
        phrase_time_limit: int = 10,
        language: str = "fr-FR",
    ) -> Optional[str]:
        """
        Listen for speech from the microphone and convert to text.

        Args:
            timeout: How long to wait for speech to start (seconds)
            phrase_time_limit: How long to record each phrase (seconds)
            language: Language code for recognition (default: French)

        Returns:
            str: Recognized text or None if no speech detected
        """
        try:
            with sr.Microphone() as source:
                self._calibrate_microphone(source)

                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )

            # Run speech recognition in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(
                None, self._recognize_speech, audio, language
            )

            return text

        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            raise Exception(f"Error during speech recognition: {str(e)}")

    def _recognize_speech(self, audio, language: str) -> Optional[str]:
        """
        Recognize speech from audio data.

        Args:
            audio: Audio data from microphone
            language: Language code for recognition

        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            # Try Google Speech Recognition (free tier)
            text = self.recognizer.recognize_google(audio, language=language)
            return text

        except sr.UnknownValueError:
            # Speech was unintelligible
            return None
        except sr.RequestError as e:
            # Could not request results from Google Speech Recognition
            raise Exception(f"Google Speech Recognition error: {str(e)}")

    async def recognize_from_file(
        self, audio_file_path: str, language: str = "fr-FR"
    ) -> Optional[str]:
        """
        Recognize speech from an audio file.

        Args:
            audio_file_path: Path to the audio file
            language: Language code for recognition

        Returns:
            str: Recognized text or None if recognition failed
        """
        try:
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)

            # Run speech recognition in a thread
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(
                None, self._recognize_speech, audio, language
            )

            return text

        except Exception as e:
            raise Exception(f"Error recognizing speech from file: {str(e)}")

    def get_microphone_info(self) -> Dict[str, Any]:
        """Get information about available microphones."""
        try:
            microphone_list = []
            for index, name in enumerate(
                sr.Microphone.list_microphone_names()
            ):
                microphone_list.append({"index": index, "name": name})

            # Use a temporary microphone instance to get info
            with sr.Microphone() as mic:
                return {
                    "microphones": microphone_list,
                    "default_index": mic.device_index,
                    "sample_rate": mic.SAMPLE_RATE,
                    "chunk_size": mic.CHUNK,
                }

        except Exception as e:
            return {"error": str(e)}

    def test_microphone(self) -> tuple[bool, str]:
        """Test if microphone is working.

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Test if PyAudio is working
            import pyaudio

            p = pyaudio.PyAudio()

            # Check if there are any input devices
            input_devices = []
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info["maxInputChannels"] > 0:
                    input_devices.append(device_info["name"])

            if not input_devices:
                p.terminate()
                return False, "No microphone devices found on system"

            # Test basic microphone access without requiring speech
            try:
                with sr.Microphone() as source:
                    # Just test that we can access the microphone
                    self.recognizer.adjust_for_ambient_noise(
                        source, duration=0.1
                    )
                    p.terminate()
                    return (
                        True,
                        f"✅ Microphone ready! Found {len(input_devices)} audio input devices. Click '🎤 Record' to test voice input.",
                    )
            except Exception as mic_error:
                p.terminate()
                return False, f"Cannot access microphone: {str(mic_error)}"

        except ImportError:
            return False, "PyAudio not installed. Run: pip install pyaudio"
        except OSError as e:
            return False, f"Microphone error: {str(e)}"
        except Exception as e:
            return False, f"Hardware test failed: {str(e)}"
