#!/usr/bin/env python3
"""Quick test script to verify Gemini integration with the new model."""

import asyncio
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.language_tutor.config_manager import ConfigManager
from src.language_tutor.services.dialogue_service import DialogueService


async def test_gemini():
    """Test Gemini dialogue generation."""
    print("Testing Gemini dialogue generation...")

    try:  # Initialize configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()

        print(f"LLM Provider: {config.llm_provider}")
        print(f"TTS Provider: {config.tts_provider}")

        # Initialize dialogue service
        dialogue_service = DialogueService(config)

        # Generate a simple dialogue
        print("Generating dialogue...")
        dialogue = await dialogue_service.generate_dialogue(
            topic="Commander un café", level="beginner", num_exchanges=2
        )

        print(f"Generated dialogue with {len(dialogue.messages)} messages:")
        for i, message in enumerate(dialogue.messages):
            print(f"{i + 1}. {message.role.value}: {message.content}")

        print("✅ Gemini integration successful!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_gemini())
    exit(0 if success else 1)
