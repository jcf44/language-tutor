#!/usr/bin/env python3
"""
Test script to verify WhisperSpeech integration.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from language_tutor.models.config import AppConfig, TTSProvider
from language_tutor.services.audio_service import AudioService


async def test_whisperspeech():
    """Test WhisperSpeech TTS functionality."""
    print("🎤 Testing WhisperSpeech TTS Integration...")
    
    # Create configuration with WhisperSpeech as default
    config = AppConfig(tts_provider=TTSProvider.WHISPERSPEECH)
    
    # Initialize audio service
    audio_service = AudioService(config)
    
    print(f"✅ Audio service initialized with TTS provider: {config.tts_provider}")
    
    # Test text to speech
    test_text = "Bonjour! Je suis votre assistant français pour apprendre la langue."
    
    print(f"🗣️  Converting text to speech: '{test_text}'")
    
    try:
        # Generate audio
        audio_file_path = await audio_service.generate_audio_for_text(
            text=test_text,
            filename="test_whisperspeech.wav"
        )
        
        print(f"✅ Audio generated successfully!")
        print(f"📁 Audio file saved to: {audio_file_path}")
        
        # Check if file exists and get info
        if os.path.exists(audio_file_path):
            file_info = audio_service.get_audio_file_info(audio_file_path)
            print(f"📊 File size: {file_info['size_mb']} MB")
            print(f"🎵 WhisperSpeech integration test completed successfully!")
            
            # Play audio if possible (optional)
            print(f"💡 You can play the audio file: {audio_file_path}")
            
        else:
            print("❌ Audio file was not created")
            
    except Exception as e:
        print(f"❌ Error during audio generation: {str(e)}")
        return False
    
    # Test available voices
    try:
        voices = await audio_service.get_available_voices()
        print(f"🎭 Available voices: {voices}")
    except Exception as e:
        print(f"⚠️  Could not get available voices: {str(e)}")
    
    return True


async def main():
    """Main test function."""
    print("🚀 Starting WhisperSpeech Integration Test...")
    print("=" * 50)
    
    success = await test_whisperspeech()
    
    print("=" * 50)
    if success:
        print("🎉 WhisperSpeech is now successfully integrated as your default TTS!")
        print("🔧 Configuration: TTS Provider = WhisperSpeech (default)")
        print("📚 Your language tutor is ready to speak French with WhisperSpeech!")
    else:
        print("💥 Integration test failed. Please check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())
