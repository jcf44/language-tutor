#!/usr/bin/env python3
"""Test script to verify the generate_complete_dialogue_audio method works correctly."""

import asyncio
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from language_tutor.config_manager import config_manager
from language_tutor.models.dialogue import (
    Dialogue,
    DialogueMessage,
    DialogueRole,
)
from language_tutor.services.audio_service import AudioService


async def test_generate_complete_dialogue_audio():
    """Test the generate_complete_dialogue_audio method."""
    try:
        # Load configuration
        config = config_manager.load_config()
        config_manager.validate_config(config)

        # Create audio service
        audio_service = AudioService(config)

        # Create a simple test dialogue
        test_dialogue = Dialogue(
            id="test_dialogue",
            title="Test Dialogue",
            messages=[
                DialogueMessage(
                    role=DialogueRole.USER,
                    content="Bonjour, comment allez-vous?",
                ),
                DialogueMessage(
                    role=DialogueRole.ASSISTANT,
                    content="Bonjour! Je vais très bien, merci. Et vous?",
                ),
            ],
        )

        print("Testing generate_complete_dialogue_audio method...")
        print(
            f"Method exists: {hasattr(audio_service, 'generate_complete_dialogue_audio')}"
        )

        if hasattr(audio_service, "generate_complete_dialogue_audio"):
            print(
                "✅ SUCCESS: generate_complete_dialogue_audio method exists!"
            )

            # Test that the method signature is correct
            import inspect

            sig = inspect.signature(
                audio_service.generate_complete_dialogue_audio
            )
            print(f"Method signature: {sig}")

            # Check if method is async
            is_async = inspect.iscoroutinefunction(
                audio_service.generate_complete_dialogue_audio
            )
            print(f"Is async: {is_async}")

        else:
            print(
                "❌ ERROR: generate_complete_dialogue_audio method does not exist!"
            )

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_generate_complete_dialogue_audio())
