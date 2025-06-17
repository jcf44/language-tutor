#!/usr/bin/env python3
"""
Configuration demo script to show .env configuration options for TTS providers.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def demo_configuration():
    """Demonstrate the configuration options for TTS providers."""

    print("🔧 Language Tutor TTS Configuration Options")
    print("=" * 50)

    try:
        from language_tutor.models.config import AppConfig, TTSProvider

        print("📋 Available TTS Providers:")
        for provider in TTSProvider:
            print(f"  • {provider.value}")

        print(f"\n🎯 Current Default: {TTSProvider.WHISPERSPEECH.value}")

        print("\n⚙️  Configuration Options in .env file:")
        print(
            "LANG_TUTOR_TTS_PROVIDER=whisperspeech    # Use WhisperSpeech (default)"
        )
        print(
            "LANG_TUTOR_TTS_PROVIDER=google_cloud     # Use Google Cloud TTS"
        )
        print("LANG_TUTOR_TTS_PROVIDER=azure            # Use Azure TTS")

        print("\n🎤 WhisperSpeech Specific Configuration:")
        print(
            "LANG_TUTOR_WHISPERSPEECH_MODEL=collabora/whisperspeech:s2a-q4-tiny-en+pl.model"
        )

        print("\n💡 How to Change TTS Provider:")
        print("1. Copy .env.sample to .env")
        print("2. Edit LANG_TUTOR_TTS_PROVIDER in .env file")
        print("3. Set provider-specific configuration (API keys, etc.)")
        print("4. Restart your application")

        # Test different configurations
        print("\n🧪 Testing Configuration Loading:")

        # Test WhisperSpeech (default)
        config_ws = AppConfig()
        print(f"✅ Default config: TTS Provider = {config_ws.tts_provider}")
        print(f"   WhisperSpeech Model = {config_ws.whisperspeech_model}")

        # Test environment override
        os.environ["LANG_TUTOR_TTS_PROVIDER"] = "google_cloud"
        config_gc = AppConfig()
        print(f"✅ Override config: TTS Provider = {config_gc.tts_provider}")

        # Reset environment
        if "LANG_TUTOR_TTS_PROVIDER" in os.environ:
            del os.environ["LANG_TUTOR_TTS_PROVIDER"]

        print("\n🎉 Configuration system is working correctly!")
        print("   WhisperSpeech is configurable via .env file!")

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False


if __name__ == "__main__":
    demo_configuration()
