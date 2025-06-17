#!/usr/bin/env python3
"""Test voice differentiation between user and assistant roles."""

import asyncio
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from language_tutor.api.tts_client import GTTSClient


async def test_voice_differentiation():
    """Test if different voices are used for user vs assistant."""
    print("Testing voice differentiation...")

    client = GTTSClient()

    test_text = "Bonjour, comment allez-vous?"

    try:
        print("Generating audio with 'user' voice...")
        user_audio = await client.synthesize_speech(
            text=test_text, voice_name="user"
        )
        print(f"User audio size: {len(user_audio)} bytes")

        print("Generating audio with 'assistant' voice...")
        assistant_audio = await client.synthesize_speech(
            text=test_text, voice_name="assistant"
        )
        print(f"Assistant audio size: {len(assistant_audio)} bytes")

        # Compare if the audio is different
        if user_audio == assistant_audio:
            print("❌ PROBLEM: Both voices generated identical audio!")
        else:
            print("✅ SUCCESS: Different voices generated different audio!")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_voice_differentiation())
