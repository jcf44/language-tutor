# Tests Directory

This directory contains test files for the Language Tutor project.

## Test Files

- `test_whisperspeech.py` - Complete WhisperSpeech TTS integration test
- `verify_integration.py` - Basic integration verification test  
- `test_core_integration.py` - Core component integration test

## Running Tests

From the project root directory:

```bash
# Run a specific test
python tests/test_whisperspeech.py

# Or run from the tests directory
cd tests
python test_whisperspeech.py
```

Note: These tests may require updating the Python path to import the project modules correctly.
