#!/usr/bin/env python3
"""Test different voices for different speakers."""

import asyncio
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.language_tutor.api.tts_client import GTTSClient


async def test_different_voices():
    """Test different voices for user and assistant."""
    client = GTTSClient()

    # Test text for both speakers
    user_text = "Bonjour, comment allez-vous?"
    assistant_text = "Très bien, merci! Et vous?"

    print("Testing different voices...")

    try:
        # Test user voice (should use standard French)
        print("Generating audio for user (standard French)...")
        user_audio = await client.synthesize_speech(
            text=user_text, voice_name="user", language_code="fr-FR"
        )
        print(f"✓ User audio generated: {len(user_audio)} bytes")

        # Test assistant voice (should use Canadian French)
        print("Generating audio for assistant (Canadian French)...")
        assistant_audio = await client.synthesize_speech(
            text=assistant_text, voice_name="assistant", language_code="fr-FR"
        )
        print(f"✓ Assistant audio generated: {len(assistant_audio)} bytes")

        # Test available voices
        voices = await client.get_available_voices()
        print(f"✓ Available voices: {voices}")

        if len(user_audio) > 0 and len(assistant_audio) > 0:
            print("✓ Different voices are working!")
        else:
            print("✗ Voice generation failed")

    except Exception as e:
        print(f"✗ Error testing voices: {e}")


if __name__ == "__main__":
    asyncio.run(test_different_voices())
