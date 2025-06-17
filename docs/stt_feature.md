# Speech-to-Text (STT) Feature

## Overview
The French Language Tutor now includes Speech-to-Text functionality, allowing you to practice speaking French directly with the application.

## Features
- **Voice Input**: Speak in French instead of typing
- **Real-time Recognition**: Automatic conversion of speech to text
- **Microphone Testing**: Built-in microphone test functionality
- **French Language Support**: Optimized for French speech recognition

## How to Use

### In Practice Mode:
1. Start a new practice session
2. When prompted for input, you can either:
   - Type your response in the text box, OR
   - Click "🎤 Record" and speak in French

### Voice Input Steps:
1. **Test Microphone**: Click "🔧 Test Mic" to verify your microphone is working
2. **Record Speech**: Click "🎤 Record" and speak clearly in French
3. **Automatic Recognition**: The app will convert your speech to text
4. **Continue Conversation**: The recognized text will be processed like typed input

## Tips for Best Results

### Hardware:
- Use a good quality microphone or headset
- Ensure your microphone is properly connected
- Grant microphone permissions when prompted by your browser

### Speaking:
- Speak clearly and at normal pace
- Use proper French pronunciation
- Minimize background noise
- Speak for 2-10 seconds for best recognition

### Environment:
- Use in a quiet environment
- Avoid echo and background noise
- Position microphone appropriately

## Troubleshooting

### "Microphone not detected":
- Check microphone connections
- Verify microphone permissions in browser
- Test microphone with other applications

### "No speech detected":
- Speak louder or closer to microphone
- Check for background noise
- Ensure you're speaking French
- Try the microphone test first

### Poor recognition accuracy:
- Speak more clearly
- Use standard French pronunciation
- Avoid rapid speech
- Try reducing background noise

## Technical Details

### Supported Platforms:
- Windows, macOS, Linux
- Modern web browsers with microphone access

### Recognition Engine:
- Google Speech Recognition API (free tier)
- Optimized for French language (fr-FR)
- Real-time processing

### Privacy:
- Audio is processed for speech recognition only
- No audio data is permanently stored
- Recognition happens through Google's API

## Dependencies
- `speechrecognition>=3.10.0`
- `pyaudio>=0.2.11`
- Working microphone and audio drivers
