#!/usr/bin/env python3
"""Microphone diagnostic utility for troubleshooting STT issues."""

import os
import sys


def check_pyaudio():
    """Check if PyAudio is installed and working."""
    try:
        import pyaudio

        print("✅ PyAudio is installed")

        p = pyaudio.PyAudio()
        print(f"✅ PyAudio initialized successfully")

        # List all audio devices
        device_count = p.get_device_count()
        print(f"Found {device_count} audio devices:")

        input_devices = []
        output_devices = []

        for i in range(device_count):
            try:
                device_info = p.get_device_info_by_index(i)
                device_name = device_info["name"]
                max_input = device_info["maxInputChannels"]
                max_output = device_info["maxOutputChannels"]

                print(f"  Device {i}: {device_name}")
                print(f"    Input channels: {max_input}")
                print(f"    Output channels: {max_output}")

                if max_input > 0:
                    input_devices.append((i, device_name))
                if max_output > 0:
                    output_devices.append((i, device_name))

            except Exception as e:
                print(f"  Device {i}: Error reading device info - {e}")

        print(f"\n📥 Input devices (microphones): {len(input_devices)}")
        for idx, name in input_devices:
            print(f"  - Device {idx}: {name}")

        print(f"\n📤 Output devices (speakers): {len(output_devices)}")
        for idx, name in output_devices:
            print(f"  - Device {idx}: {name}")

        # Check default devices
        try:
            default_input = p.get_default_input_device_info()
            print(f"\n🎤 Default input device: {default_input['name']}")
        except Exception as e:
            print(f"\n❌ No default input device: {e}")

        try:
            default_output = p.get_default_output_device_info()
            print(f"🔊 Default output device: {default_output['name']}")
        except Exception as e:
            print(f"❌ No default output device: {e}")

        p.terminate()

        if not input_devices:
            print("\n❌ No microphone devices found!")
            print("Possible solutions:")
            print("  - Connect a microphone or headset")
            print("  - Check Windows audio settings")
            print("  - Update audio drivers")
            print("  - Set a default input device in Windows")
            return False
        else:
            print(f"\n✅ Found {len(input_devices)} microphone device(s)")
            return True

    except ImportError:
        print("❌ PyAudio not installed")
        print("Install with: uv add pyaudio")
        return False
    except Exception as e:
        print(f"❌ PyAudio error: {e}")
        return False


def check_speech_recognition():
    """Check if speech_recognition is installed."""
    try:
        import speech_recognition as sr

        print("✅ speech_recognition is installed")

        # Test recognizer creation
        r = sr.Recognizer()
        print("✅ Speech recognizer created successfully")

        # Test microphone creation
        m = sr.Microphone()
        print("✅ Microphone object created successfully")

        return True
    except ImportError:
        print("❌ speech_recognition not installed")
        print("Install with: uv add speechrecognition")
        return False
    except Exception as e:
        print(f"❌ speech_recognition error: {e}")
        return False


def main():
    """Run microphone diagnostics."""
    print("🔍 Language Tutor - Microphone Diagnostics")
    print("=" * 50)

    print("\n1. Checking Python packages...")
    sr_ok = check_speech_recognition()
    pyaudio_ok = check_pyaudio()

    print("\n" + "=" * 50)
    print("📋 SUMMARY:")

    if sr_ok and pyaudio_ok:
        print("✅ All packages are installed correctly")
        print("✅ Microphone hardware detected")
        print("\n💡 If voice input still doesn't work:")
        print("  - Make sure browser allows microphone access")
        print("  - Try speaking louder and clearer")
        print("  - Check if microphone is muted")
        print("  - Test with another application first")
    else:
        print("❌ Issues found with packages or hardware")
        print("\n🔧 Fix the issues above, then restart the app")


if __name__ == "__main__":
    main()
