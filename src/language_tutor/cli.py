"""Command line interface for the Language Tutor application."""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path

from .config_manager import config_manager


def run_streamlit():
    """Run the Streamlit web interface."""
    print("Starting Language Tutor Web Interface...")
    print("Open your browser and go to the URL shown below.")

    # Get the path to the streamlit app
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_app_path = os.path.join(current_dir, "ui", "streamlit_app.py")

    # Run streamlit using subprocess
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", streamlit_app_path]
        )
    except KeyboardInterrupt:
        print("\nShutting down Language Tutor...")
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        print("Please ensure Streamlit is installed: pip install streamlit")


def setup_config():
    """Set up configuration files."""
    config_manager.create_sample_env_file()
    print("\nConfiguration setup completed!")
    print(
        "Please edit the .env file with your API keys before running the application."
    )


def validate_config():
    """Validate the current configuration."""
    try:
        config = config_manager.load_config()
        config_manager.validate_config(config)
        print("✅ Configuration is valid!")
        print(f"LLM Provider: {config.llm_provider.value}")
        print(f"TTS Provider: {config.tts_provider.value}")

    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="French Practice AI Application - Language Tutor"
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the web interface")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up configuration")

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate configuration"
    )

    args = parser.parse_args()

    if args.command == "run":
        run_streamlit()
    elif args.command == "setup":
        setup_config()
    elif args.command == "validate":
        validate_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    main()
