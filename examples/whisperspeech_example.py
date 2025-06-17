"""
WhisperSpeech Text-to-Speech Example
====================================

This example demonstrates how to use WhisperSpeech for text-to-speech generation.
WhisperSpeech is a modern, open-source TTS system that produces high-quality audio.
"""

import torch
from whisperspeech.pipeline import Pipeline


def main():
    # Initialize WhisperSpeech pipeline
    # This will download models on first use
    print("Initializing WhisperSpeech pipeline...")
    pipe = Pipeline(s2a_ref="collabora/whisperspeech:s2a-q4-tiny-en+pl.model")

    # Text to convert to speech
    text = "Bonjour! Comment allez-vous? Je suis ravi de pratiquer le français avec vous."

    print(f"Converting text to speech: {text}")

    # Generate speech
    # The generate method returns a torch tensor with the audio
    audio_tensor = pipe.generate(text)

    # Convert to numpy array for saving or playback
    audio_np = audio_tensor.cpu().numpy()

    print(f"Generated audio with shape: {audio_np.shape}")
    print(f"Sample rate: {pipe.sample_rate} Hz")

    # Save the audio to a file
    import torchaudio

    output_path = "output_speech.wav"

    # WhisperSpeech generates at 24kHz by default
    torchaudio.save(output_path, audio_tensor.unsqueeze(0), pipe.sample_rate)
    print(f"Audio saved to: {output_path}")


def generate_multilingual_speech():
    """Example showing multilingual capabilities"""
    print("\n--- Multilingual Speech Generation ---")

    pipe = Pipeline()

    texts = [
        "Hello, this is English text.",
        "Bonjour, c'est du texte français.",
        "Dzień dobry, to jest tekst po polsku.",  # Polish example
    ]

    for i, text in enumerate(texts):
        print(f"Generating speech for: {text}")
        audio = pipe.generate(text)

        # Save each file
        import torchaudio

        filename = f"multilingual_example_{i + 1}.wav"
        torchaudio.save(filename, audio.unsqueeze(0), pipe.sample_rate)
        print(f"Saved: {filename}")


def voice_cloning_example():
    """Example showing voice cloning capabilities"""
    print("\n--- Voice Cloning Example ---")

    # For voice cloning, you would provide a reference audio file
    # This is a basic example - refer to WhisperSpeech documentation for full voice cloning
    pipe = Pipeline()

    text = "This text will be spoken in a cloned voice."

    # Basic generation (without reference audio in this example)
    audio = pipe.generate(text)

    import torchaudio

    torchaudio.save(
        "voice_clone_example.wav", audio.unsqueeze(0), pipe.sample_rate
    )
    print("Voice cloning example saved as: voice_clone_example.wav")


if __name__ == "__main__":
    main()
    generate_multilingual_speech()
    voice_cloning_example()
