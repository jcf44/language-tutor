# French Practice AI Application - Language Tutor 🇫🇷

A comprehensive Python-based application designed to help users practice French through conversational interactions, featuring AI-generated dialogues and high-quality text-to-speech audio.

## Features

### 🤖 AI-Powered Dialogue Generation

- Generate natural French dialogues using OpenAI GPT-4 or Google Gemini
- Customizable difficulty levels (beginner, intermediate, advanced)
- Contextual dialogue generation with custom prompts
- Configurable dialogue length and topics

### 🔊 High-Quality Text-to-Speech

- Integration with Google Cloud Text-to-Speech and Azure Cognitive Services
- Multiple French voice profiles and genders
- High-fidelity MP3 audio output
- Individual message audio and complete dialogue audio

### 📁 Flexible Dialogue Import/Export

- Support for multiple file formats: TXT, JSON, CSV, MD
- Easy upload and processing of custom dialogues
- Export generated dialogues in various formats
- Proper handling of French characters and formatting

### 💬 Interactive Practice Mode

- Real-time conversation practice with AI
- Context-aware responses
- Instant audio feedback
- Progressive dialogue building

### 🎵 Audio Library Management

- Organized audio file management
- Individual message playbook
- Complete dialogue audio generation
- Download and export capabilities

## Project Structure

```
language-tutor/
├── src/
│   └── language_tutor/
│       ├── models/          # Data models and configuration
│       │   ├── __init__.py
│       │   ├── config.py    # Application configuration
│       │   └── dialogue.py  # Dialogue data models
│       ├── api/             # External API clients
│       │   ├── __init__.py
│       │   ├── llm_client.py    # LLM API wrappers
│       │   └── tts_client.py    # TTS API wrappers
│       ├── services/        # Business logic
│       │   ├── __init__.py
│       │   ├── dialogue_service.py  # Dialogue management
│       │   ├── file_service.py      # File operations
│       │   └── audio_service.py     # Audio generation
│       ├── ui/              # User interface
│       │   ├── __init__.py
│       │   └── streamlit_app.py     # Web interface
│       ├── __init__.py
│       ├── config_manager.py        # Configuration management
│       └── cli.py                   # Command line interface
├── sample_dialogues/        # Sample dialogue files
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended) or `pip`

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd language-tutor
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. **Set up configuration**

   ```bash
   # Generate sample configuration
   language-tutor setup
   ```

4. **Configure API keys**
   Edit the `.env` file with your API keys:

   ```env
   # LLM Provider (choose one)
   LANG_TUTOR_LLM_PROVIDER=openai
   LANG_TUTOR_OPENAI_API_KEY=your_openai_api_key_here
   # OR
   LANG_TUTOR_LLM_PROVIDER=gemini
   LANG_TUTOR_GEMINI_API_KEY=your_gemini_api_key_here

   # TTS Provider (choose one)
   LANG_TUTOR_TTS_PROVIDER=google_cloud
   LANG_TUTOR_GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/credentials.json
   # OR
   LANG_TUTOR_TTS_PROVIDER=azure
   LANG_TUTOR_AZURE_SPEECH_KEY=your_azure_speech_key
   LANG_TUTOR_AZURE_SPEECH_REGION=your_azure_region
   ```

5. **Validate configuration**

   ```bash
   language-tutor validate
   ```

## Usage

### Running the Web Interface

```bash
# Start the Streamlit web application
language-tutor run
```

The application will be available at `http://localhost:8501`

### Web Interface Features

#### 1. Generate Dialogue Tab

- Enter a topic and context for dialogue generation
- Select difficulty level and number of exchanges
- Generate AI-powered French dialogues
- Automatic audio generation option

#### 2. Import Dialogue Tab

- Upload dialogue files in supported formats
- Automatic format detection and parsing
- Generate audio for imported dialogues

#### 3. Practice Mode Tab

- Interactive conversation practice
- Real-time AI responses
- Audio feedback for each response
- Context-aware dialogue continuation

#### 4. Audio Library Tab

- Browse and play generated audio files
- Export dialogues in various formats
- Download individual or complete dialogue audio

### Supported File Formats

#### Text Format (.txt, .md)

```
Speaker 1: Bonjour, comment allez-vous ?
Speaker 2: Je vais bien, merci. Et vous ?
```

#### JSON Format (.json)

```json
{
  "title": "Greeting Dialogue",
  "level": "beginner",
  "messages": [
    {"role": "user", "content": "Bonjour !"},
    {"role": "assistant", "content": "Bonjour, comment allez-vous ?"}
  ]
}
```

#### CSV Format (.csv)

```csv
speaker,message
user,"Bonjour !"
assistant,"Bonjour, comment allez-vous ?"
```

## API Configuration

### OpenAI Configuration

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Set `LANG_TUTOR_LLM_PROVIDER=openai`
3. Set `LANG_TUTOR_OPENAI_API_KEY=your_key`

### Google Gemini Configuration

1. Get an API key from [Google AI Studio](https://makersuite.google.com/)
2. Set `LANG_TUTOR_LLM_PROVIDER=gemini`
3. Set `LANG_TUTOR_GEMINI_API_KEY=your_key`

### Google Cloud TTS Configuration

1. Set up a Google Cloud project
2. Enable the Text-to-Speech API
3. Download service account credentials
4. Set `LANG_TUTOR_TTS_PROVIDER=google_cloud`
5. Set `LANG_TUTOR_GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/credentials.json`

### Azure Cognitive Services Configuration

1. Create an Azure Cognitive Services resource
2. Get the API key and region
3. Set `LANG_TUTOR_TTS_PROVIDER=azure`
4. Set `LANG_TUTOR_AZURE_SPEECH_KEY=your_key`
5. Set `LANG_TUTOR_AZURE_SPEECH_REGION=your_region`

## Sample Dialogues

The `sample_dialogues/` directory contains example files in different formats:

- `sample_restaurant.txt` - Restaurant conversation (text format)
- `sample_shopping.json` - Shopping dialogue (JSON format)
- `sample_directions.csv` - Asking for directions (CSV format)

Use these files to test the import functionality.

## Development

### Architecture

The application follows a clean architecture with separation of concerns:

- **Models**: Data structures and configuration (Pydantic models)
- **API**: External service integrations (OpenAI, Gemini, Google Cloud, Azure)
- **Services**: Business logic and orchestration
- **UI**: User interface (Streamlit web app)

### Key Components

1. **LLM Clients**: Abstracted interface for different language models
2. **TTS Clients**: Abstracted interface for text-to-speech services
3. **Dialogue Service**: Manages dialogue generation and continuation
4. **File Service**: Handles import/export operations
5. **Audio Service**: Manages audio generation and file operations
6. **Configuration Manager**: Centralized configuration management

### Adding New Providers

To add a new LLM or TTS provider:

1. Create a new client class implementing the respective interface
2. Update the configuration models
3. Add the provider to the service factory methods
4. Update the configuration documentation

## Troubleshooting

### Common Issues

1. **Configuration Error**: Ensure all required API keys are set in the `.env` file
2. **Audio Generation Failed**: Check TTS provider credentials and network connectivity
3. **Dialogue Generation Failed**: Verify LLM provider API key and quota
4. **Import Error**: Ensure file format is supported and properly formatted

### Performance Considerations

- Dialogue generation typically takes 2-5 seconds
- Audio synthesis may take 1-3 seconds per message
- Large dialogues may require more processing time
- API rate limits may affect performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT API
- Google for Gemini and Cloud TTS APIs
- Microsoft Azure for Cognitive Services
- Streamlit for the web framework
- All contributors to the open-source libraries used
