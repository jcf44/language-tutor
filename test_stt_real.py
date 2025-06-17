#!/usr/bin/env python3
"""Test actual STT functionality."""

import asyncio
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


async def test_stt_real():
    """Test real STT functionality."""
    try:
        from language_tutor.config_manager import config_manager
        from language_tutor.services.stt_service import STTService

        print("Testing Real STT Functionality...")

        # Load configuration
        config = config_manager.load_config()
        config_manager.validate_config(config)

        # Create STT service
        stt_service = STTService(config)
        print("✅ STT Service created")

        # Test the microphone detection
        mic_works, message = stt_service.test_microphone()
        print(f"Microphone test: {message}")

        if not mic_works:
            print(
                "❌ Microphone test failed, but let's try speech recognition anyway..."
            )

        # Try a quick speech recognition test
        print("\n🎤 Testing speech recognition...")
        print("Speak something in French in the next 5 seconds...")

        try:
            result = await stt_service.listen_for_speech(
                timeout=5, phrase_time_limit=5, language="fr-FR"
            )

            if result:
                print(f"✅ Speech recognized: '{result}'")
            else:
                print("❌ No speech detected")

        except Exception as e:
            print(f"❌ Speech recognition error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_stt_real())
