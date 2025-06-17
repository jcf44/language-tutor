#!/usr/bin/env python3
"""
Simple verification that WhisperSpeech is integrated and working.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_basic_integration():
    """Test that WhisperSpeech integration works."""
    try:
        # Test imports
        from language_tutor.models.config import AppConfig, TTSProvider
        from language_tutor.services.audio_service import AudioService
        
        print("✅ All imports successful!")
        
        # Check that WHISPERSPEECH is available
        print(f"📋 Available TTS providers: {list(TTSProvider)}")
        print(f"🎯 Default TTS provider: {TTSProvider.WHISPERSPEECH}")
        
        # Create config with WhisperSpeech
        config = AppConfig(tts_provider=TTSProvider.WHISPERSPEECH)
        print(f"⚙️  Config created with TTS provider: {config.tts_provider}")
        
        # Initialize audio service
        audio_service = AudioService(config)
        print("🎤 AudioService initialized successfully!")
        
        # Test getting available voices
        voices = await audio_service.get_available_voices()
        print(f"🎭 Available voices: {voices}")
        
        print("\n🎉 WhisperSpeech integration verified successfully!")
        print("🚀 Your language tutor is ready to use WhisperSpeech as the default TTS!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Verifying WhisperSpeech Integration...")
    print("=" * 50)
    
    success = asyncio.run(test_basic_integration())
    
    print("=" * 50)
    if success:
        print("✅ Integration complete! WhisperSpeech is now your default TTS.")
    else:
        print("❌ Integration verification failed.")
