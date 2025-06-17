#!/usr/bin/env python3
"""Test gTTS integration with proper async handling."""

import asyncio
import os
import tempfile

from src.language_tutor.api.tts_client import GTTSClient


async def test_gtts():
    """Test gTTS with French text."""
    client = GTTSClient()

    try:
        # Test French text synthesis
        audio_bytes = await client.synthesize_speech(
            "Bonjour, comment allez-vous?", language_code="fr"
        )

        if audio_bytes:
            print(f"✓ French audio generated successfully")
            print(f"Audio data size: {len(audio_bytes)} bytes")

            # Test saving to file
            temp_path = None
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False
            ) as tmp:
                temp_path = tmp.name
                tmp.write(audio_bytes)

            if os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                print(f"✓ Audio saved to file: {temp_path}")
                print(f"File size: {file_size} bytes")

                if file_size > 0:
                    print("✓ Audio file has content")
                else:
                    print("✗ Audio file is empty")

                # Clean up
                os.unlink(temp_path)
                print("✓ Temporary file cleaned up")
            else:
                print("✗ Audio file was not saved")
        else:
            print("✗ No audio data generated")

    except Exception as e:
        print(f"✗ Error during audio generation: {e}")


if __name__ == "__main__":
    asyncio.run(test_gtts())
