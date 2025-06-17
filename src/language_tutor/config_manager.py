"""Configuration management for the language tutor application."""

import os
from typing import Optional

from dotenv import load_dotenv

from .models.config import AppConfig, LLMProvider, TTSProvider


class ConfigManager:
    """Manager for application configuration."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration manager."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # Load from .env file in current directory

    def load_config(self) -> AppConfig:
        """Load configuration from environment variables."""
        return AppConfig(
            # LLM Configuration
            llm_provider=LLMProvider(
                os.getenv("LANG_TUTOR_LLM_PROVIDER", "openai")
            ),
            openai_api_key=os.getenv("LANG_TUTOR_OPENAI_API_KEY"),
            gemini_api_key=os.getenv("LANG_TUTOR_GEMINI_API_KEY"),
            # TTS Configuration
            tts_provider=TTSProvider(
                os.getenv("LANG_TUTOR_TTS_PROVIDER", "gtts")
            ),
            google_cloud_credentials_path=os.getenv(
                "LANG_TUTOR_GOOGLE_CLOUD_CREDENTIALS_PATH"
            ),
            azure_speech_key=os.getenv("LANG_TUTOR_AZURE_SPEECH_KEY"),
            azure_speech_region=os.getenv("LANG_TUTOR_AZURE_SPEECH_REGION"),
            # WhisperSpeech Configuration
            whisperspeech_model=os.getenv(
                "LANG_TUTOR_WHISPERSPEECH_MODEL",
                "collabora/whisperspeech:s2a-q4-tiny-en+pl.model",
            ),
            # General Settings
            max_dialogue_length=int(
                os.getenv("LANG_TUTOR_MAX_DIALOGUE_LENGTH", "10")
            ),
            default_voice_gender=os.getenv(
                "LANG_TUTOR_DEFAULT_VOICE_GENDER", "female"
            ),
            audio_output_format=os.getenv(
                "LANG_TUTOR_AUDIO_OUTPUT_FORMAT", "mp3"
            ),
            # Performance Settings
            request_timeout=int(os.getenv("LANG_TUTOR_REQUEST_TIMEOUT", "30")),
            max_concurrent_requests=int(
                os.getenv("LANG_TUTOR_MAX_CONCURRENT_REQUESTS", "5")
            ),
        )

    def validate_config(self, config: AppConfig) -> bool:
        """Validate that required configuration is present."""
        # Check LLM provider configuration
        if config.llm_provider == LLMProvider.OPENAI:
            if not config.openai_api_key:
                raise ValueError(
                    "OpenAI API key is required when using OpenAI provider"
                )

        elif config.llm_provider == LLMProvider.GEMINI:
            if not config.gemini_api_key:
                raise ValueError(
                    "Gemini API key is required when using Gemini provider"
                )  # Check TTS provider configuration
        if config.tts_provider == TTSProvider.GOOGLE_CLOUD:
            # Google Cloud TTS can work with default credentials
            pass

        elif config.tts_provider == TTSProvider.AZURE:
            if not config.azure_speech_key or not config.azure_speech_region:
                raise ValueError(
                    "Azure speech key and region are required when using "
                    "Azure TTS"
                )

        elif config.tts_provider == TTSProvider.WHISPERSPEECH:
            # WhisperSpeech works with default model, no validation needed
            pass

        return True

    def create_sample_env_file(self, file_path: str = ".env.sample") -> None:
        """Create a sample environment file with all configuration options."""
        sample_content = """# Language Tutor Configuration

# LLM Provider Configuration
LANG_TUTOR_LLM_PROVIDER=openai  # Options: openai, gemini
LANG_TUTOR_OPENAI_API_KEY=your_openai_api_key_here
LANG_TUTOR_GEMINI_API_KEY=your_gemini_api_key_here

# TTS Provider Configuration
LANG_TUTOR_TTS_PROVIDER=google_cloud  # Options: google_cloud, azure
LANG_TUTOR_GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/credentials.json
LANG_TUTOR_AZURE_SPEECH_KEY=your_azure_speech_key_here
LANG_TUTOR_AZURE_SPEECH_REGION=your_azure_region_here

# General Settings
LANG_TUTOR_MAX_DIALOGUE_LENGTH=10
LANG_TUTOR_DEFAULT_VOICE_GENDER=female
LANG_TUTOR_AUDIO_OUTPUT_FORMAT=mp3

# Performance Settings
LANG_TUTOR_REQUEST_TIMEOUT=30
LANG_TUTOR_MAX_CONCURRENT_REQUESTS=5
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        print(f"Sample environment file created: {file_path}")
        print("Please copy this to .env and fill in your API keys.")


# Global configuration instance
config_manager = ConfigManager()
# Global configuration instance
config_manager = ConfigManager()
