"""Configuration models for the language tutor application."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    GEMINI = "gemini"


class TTSProvider(str, Enum):
    """Supported TTS providers."""

    GOOGLE_CLOUD = "google_cloud"
    AZURE = "azure"
    WHISPERSPEECH = "whisperspeech"
    GTTS = "gtts"


class AppConfig(BaseModel):
    """Application configuration model."""  # LLM Configuration

    llm_provider: LLMProvider = Field(default=LLMProvider.GEMINI)
    openai_api_key: Optional[str] = Field(default=None)
    gemini_api_key: Optional[str] = Field(default=None)  # TTS Configuration
    tts_provider: TTSProvider = Field(default=TTSProvider.GTTS)
    google_cloud_credentials_path: Optional[str] = Field(default=None)
    azure_speech_key: Optional[str] = Field(default=None)
    azure_speech_region: Optional[str] = Field(default=None)

    # WhisperSpeech Configuration
    whisperspeech_model: Optional[str] = Field(
        default="collabora/whisperspeech:s2a-q4-tiny-en+pl.model",
        description="WhisperSpeech model to use",
    )

    # General Settings
    max_dialogue_length: int = Field(
        default=10, description="Maximum number of exchanges in a dialogue"
    )
    default_voice_gender: str = Field(
        default="female", description="Default voice gender for TTS"
    )
    audio_output_format: str = Field(
        default="mp3", description="Audio output format"
    )

    # Performance Settings
    request_timeout: int = Field(
        default=30, description="API request timeout in seconds"
    )
    max_concurrent_requests: int = Field(
        default=5, description="Maximum concurrent API requests"
    )

    class Config:
        """Pydantic config."""

        env_prefix = "LANG_TUTOR_"
        case_sensitive = False
        case_sensitive = False
