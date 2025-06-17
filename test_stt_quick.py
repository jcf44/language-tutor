#!/usr/bin/env python3
"""Quick test of STT service functionality."""

import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from language_tutor.models.config import AppConfig
from language_tutor.services.stt_service import STTService


def test_stt_service():
    """Test basic STT service functionality."""
    print("Testing STT Service...")

    # Create config and service
    config = AppConfig()
    stt_service = STTService(config)

    # Test microphone info
    print("\n1. Testing microphone info...")
    mic_info = stt_service.get_microphone_info()
    print(f"Microphone info: {mic_info}")

    # Test microphone test
    print("\n2. Testing microphone test...")
    success, message = stt_service.test_microphone()
    print(f"Microphone test - Success: {success}, Message: {message}")

    print("\nSTT Service test completed!")
    return success


if __name__ == "__main__":
    try:
        result = test_stt_service()
        if result:
            print("✅ STT Service is working correctly!")
        else:
            print(
                "❌ STT Service has issues, but they may be related to microphone hardware."
            )
    except Exception as e:
        print(f"❌ Error testing STT Service: {e}")
        sys.exit(1)
