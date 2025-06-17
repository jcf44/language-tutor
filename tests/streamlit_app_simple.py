"""Streamlit web interface for the French Language Tutor."""

import asyncio
import os
import sys
import tempfile
from typing import Any, Dict, Optional

import streamlit as st

# Set page config as the very first Streamlit command
st.set_page_config(
    page_title="French Language Tutor", page_icon="🇫🇷", layout="wide"
)

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from language_tutor.config_manager import config_manager
from language_tutor.models.dialogue import Dialogue, DialogueRole
from language_tutor.services.audio_service import AudioService
from language_tutor.services.dialogue_service import DialogueService
from language_tutor.services.file_service import FileService


class LanguageTutorUI:
    """Main UI class for the Language Tutor application."""

    def __init__(self):
        """Initialize the UI."""
        self.config = None
        self.dialogue_service = None
        self.file_service = None
        self.audio_service = None
        self._initialize_services()

    def _initialize_services(self):
        """Initialize services with configuration."""
        self.config = config_manager.load_config()
        config_manager.validate_config(self.config)
        self.dialogue_service = DialogueService(self.config)
        self.file_service = FileService()
        self.audio_service = AudioService(self.config)

    def run(self):
        """Run the Streamlit application."""
        st.title("🇫🇷 French Language Tutor")
        st.markdown(
            "*Practice French through AI-generated dialogues with high-quality audio*"
        )

        # Configuration display
        st.sidebar.title("⚙️ Configuration")
        st.sidebar.info(f"LLM Provider: {self.config.llm_provider.value}")
        st.sidebar.info(f"TTS Provider: {self.config.tts_provider.value}")

        if self.config.tts_provider.value == "whisperspeech":
            st.sidebar.info(
                f"WhisperSpeech Model: {self.config.whisperspeech_model}"
            )

        # Simple test interface
        st.header("🎤 TTS Test")
        test_text = st.text_input(
            "Enter text to convert to speech:", "Bonjour! Comment allez-vous?"
        )

        if st.button("🔊 Generate Audio"):
            if test_text:
                with st.spinner("Generating audio..."):
                    try:
                        # Test audio generation
                        audio_file = asyncio.run(
                            self.audio_service.generate_audio_for_text(
                                test_text
                            )
                        )
                        st.success("Audio generated successfully!")
                        st.audio(audio_file)
                    except Exception as e:
                        st.error(f"Error generating audio: {str(e)}")
            else:
                st.warning("Please enter some text to convert to speech.")

        # Status information
        st.header("📊 System Status")
        st.success("✅ Configuration loaded successfully")
        st.success("✅ WhisperSpeech TTS provider active")
        st.success("✅ All services initialized")


def main():
    """Main entry point for the Streamlit app."""
    try:
        ui = LanguageTutorUI()
        ui.run()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()
