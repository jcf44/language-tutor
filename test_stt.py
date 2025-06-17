#!/usr/bin/env python3
"""Test STT service functionality."""

import asyncio
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from language_tutor.config_manager import config_manager
    from language_tutor.services.stt_service import STTService
    
    async def test_stt_service():
        """Test the STT service basic functionality."""
        print("Testing STT Service...")
        
        try:
            # Load configuration
            config = config_manager.load_config()
            config_manager.validate_config(config)
            
            # Create STT service
            stt_service = STTService(config)
            
            print("✅ STT Service created successfully!")
            
            # Test microphone info
            mic_info = stt_service.get_microphone_info()
            print(f"Available microphones: {len(mic_info.get('microphones', []))}")
            
            # Test microphone
            mic_works = stt_service.test_microphone()
            print(f"Microphone test: {'✅ PASS' if mic_works else '❌ FAIL'}")
            
            if mic_works:
                print("🎤 You can now use voice input in the Practice Mode!")
            else:
                print("⚠️  Microphone not working. Voice input may not be available.")
                
        except Exception as e:
            print(f"❌ Error testing STT service: {str(e)}")
    
    if __name__ == "__main__":
        asyncio.run(test_stt_service())
        
except ImportError as e:
    print(f"❌ Import error: {str(e)}")
    print("Make sure all dependencies are installed with: uv sync")
