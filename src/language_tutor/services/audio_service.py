"""Service for handling audio generation and management."""

import asyncio
import os
from typing import Any, Dict, List, Optional

from ..api.tts_client import (
    AzureTTSClient,
    GoogleCloudTTSClient,
    GTTSClient,
    TTSClient,
    WhisperSpeechTTSClient,
    create_temp_audio_file,
    save_audio_file,
)
from ..models.config import AppConfig, TTSProvider
from ..models.dialogue import Dialogue, DialogueMessage


class AudioService:
    """Service for audio generation and management."""

    def __init__(self, config: AppConfig):
        """Initialize the audio service with configuration."""
        self.config = config
        self.tts_client = self._create_tts_client()
        self.output_directory = "audio_output"
        os.makedirs(self.output_directory, exist_ok=True)

    def _create_tts_client(self) -> TTSClient:
        """Create appropriate TTS client based on configuration."""
        if self.config.tts_provider == TTSProvider.GOOGLE_CLOUD:
            return GoogleCloudTTSClient(
                credentials_path=self.config.google_cloud_credentials_path
            )
        elif self.config.tts_provider == TTSProvider.AZURE:
            if (
                not self.config.azure_speech_key
                or not self.config.azure_speech_region
            ):
                raise ValueError("Azure speech key and region are required")
            return AzureTTSClient(
                speech_key=self.config.azure_speech_key,
                speech_region=self.config.azure_speech_region,
            )

        elif self.config.tts_provider == TTSProvider.WHISPERSPEECH:
            return WhisperSpeechTTSClient(
                model_ref=self.config.whisperspeech_model
            )

        elif self.config.tts_provider == TTSProvider.GTTS:
            return GTTSClient()

        else:
            raise ValueError(
                f"Unsupported TTS provider: {self.config.tts_provider}"
            )

    async def generate_audio_for_text(
        self,
        text: str,
        voice_name: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> str:
        """Generate audio for a single text and return file path."""
        try:
            # Synthesize speech
            audio_data = await self.tts_client.synthesize_speech(
                text=text, voice_name=voice_name
            )

            # Create filename if not provided
            if not filename:
                # Create safe filename from text (first 50 chars)
                safe_text = "".join(
                    c for c in text[:50] if c.isalnum() or c in (" ", "-", "_")
                ).rstrip()
                filename = f"{safe_text}.wav"  # Save audio to file
            file_path = await save_audio_file(audio_data, filename)

            return file_path

        except Exception as e:
            raise Exception(f"Error generating audio: {str(e)}")

    async def generate_audio_for_dialogue(
        self, dialogue: Dialogue, voice_name: Optional[str] = None
    ) -> Dialogue:
        """Generate audio for all messages in a dialogue that don't have audio."""
        try:
            # Process each message
            for i, message in enumerate(dialogue.messages):
                # Generate audio for all messages (both user and assistant)
                # since in French learning, both sides speak French
                if not message.audio_file_path and message.content.strip():
                    filename = f"dialogue_{dialogue.id}_message_{i}.wav"

                    # Use different voice names for different speakers
                    speaker_voice = voice_name or message.role.value

                    # Generate audio for this message with role-specific voice
                    file_path = await self.generate_audio_for_text(
                        text=message.content,
                        voice_name=speaker_voice,
                        filename=filename,
                    )

                    # Update message with audio file path
                    message.audio_file_path = file_path

            return dialogue

        except Exception as e:
            raise Exception(f"Error generating dialogue audio: {str(e)}")

    async def get_available_voices(
        self, language_code: str = "fr-FR"
    ) -> List[str]:
        """Get list of available voices for the current TTS provider."""
        try:
            return await self.tts_client.get_available_voices(language_code)
        except Exception as e:
            raise Exception(f"Error getting available voices: {str(e)}")

    async def create_temporary_audio(
        self, text: str, voice_name: Optional[str] = None
    ) -> str:
        """Create temporary audio file for immediate playback."""
        try:
            # Synthesize speech
            audio_data = await self.tts_client.synthesize_speech(
                text=text, voice_name=voice_name
            )

            # Create temporary file
            temp_file_path = await create_temp_audio_file(audio_data)

            return temp_file_path

        except Exception as e:
            raise Exception(f"Error creating temporary audio: {str(e)}")

    def list_audio_files(self) -> List[Dict[str, Any]]:
        """List all audio files in the output directory."""
        try:
            audio_files = []

            if not os.path.exists(self.output_directory):
                return audio_files

            for filename in os.listdir(self.output_directory):
                if filename.endswith((".mp3", ".wav", ".m4a")):
                    file_path = os.path.join(self.output_directory, filename)
                    file_info = self.get_audio_file_info(file_path)
                    file_info["filename"] = filename
                    file_info["file_path"] = file_path
                    audio_files.append(file_info)

            # Sort by creation time (newest first)
            audio_files.sort(
                key=lambda x: x.get("created_at", 0), reverse=True
            )

            return audio_files

        except Exception as e:
            raise Exception(f"Error listing audio files: {str(e)}")

    def delete_audio_file(self, file_path: str) -> bool:
        """Delete an audio file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            raise Exception(f"Error deleting audio file: {str(e)}")

    def cleanup_old_files(self, max_files: int = 100) -> int:
        """Clean up old audio files, keeping only the most recent ones."""
        try:
            audio_files = self.list_audio_files()

            if len(audio_files) <= max_files:
                return 0

            # Delete oldest files
            files_to_delete = audio_files[max_files:]
            deleted_count = 0

            for file_info in files_to_delete:
                if self.delete_audio_file(file_info["file_path"]):
                    deleted_count += 1

            return deleted_count

        except Exception as e:
            raise Exception(f"Error cleaning up files: {str(e)}")

    def cleanup_dialogue_audio(self, dialogue: Dialogue):
        """Clean up audio files associated with a dialogue."""
        for message in dialogue.messages:
            if message.audio_file_path:
                try:
                    if os.path.exists(message.audio_file_path):
                        os.remove(message.audio_file_path)
                        message.audio_file_path = None
                except OSError:
                    pass  # Ignore cleanup errors

    def get_audio_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about an audio file."""
        if not os.path.exists(file_path):
            return {"exists": False}

        file_stats = os.stat(file_path)

        return {
            "exists": True,
            "size_bytes": file_stats.st_size,
            "size_mb": round(file_stats.st_size / (1024 * 1024), 2),
            "created_at": file_stats.st_ctime,
            "modified_at": file_stats.st_mtime,
        }
