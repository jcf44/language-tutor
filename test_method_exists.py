#!/usr/bin/env python3
"""Simple test to verify the generate_complete_dialogue_audio method exists."""

import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from language_tutor.services.audio_service import AudioService

    print("Testing generate_complete_dialogue_audio method...")
    print(
        f"Method exists: {hasattr(AudioService, 'generate_complete_dialogue_audio')}"
    )

    if hasattr(AudioService, "generate_complete_dialogue_audio"):
        print("✅ SUCCESS: generate_complete_dialogue_audio method exists!")

        # Test that the method signature is correct
        import inspect

        sig = inspect.signature(AudioService.generate_complete_dialogue_audio)
        print(f"Method signature: {sig}")

        # Check if method is async
        is_async = inspect.iscoroutinefunction(
            AudioService.generate_complete_dialogue_audio
        )
        print(f"Is async: {is_async}")

    else:
        print(
            "❌ ERROR: generate_complete_dialogue_audio method does not exist!"
        )

except Exception as e:
    print(f"❌ ERROR importing AudioService: {str(e)}")
