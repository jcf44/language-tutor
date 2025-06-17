#!/usr/bin/env python3
"""Setup script for the French Language Tutor application."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.12 or higher."""
    if sys.version_info < (3, 12):
        print("❌ Python 3.12 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def check_uv_installed():
    """Check if uv is installed."""
    if shutil.which("uv"):
        print("✅ uv package manager found")
        return True
    else:
        print("⚠️ uv package manager not found")
        print("Install uv with: pip install uv")
        return False


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")

    if check_uv_installed():
        try:
            subprocess.run(["uv", "sync"], check=True)
            print("✅ Dependencies installed with uv")
        except subprocess.CalledProcessError:
            print("❌ Failed to install with uv, trying pip...")
            install_with_pip()
    else:
        install_with_pip()


def install_with_pip():
    """Install dependencies with pip."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."], check=True
        )
        print("✅ Dependencies installed with pip")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def setup_config():
    """Set up configuration files."""
    print("⚙️ Setting up configuration...")

    env_sample = Path(".env.sample")
    env_file = Path(".env")

    if env_sample.exists() and not env_file.exists():
        shutil.copy(env_sample, env_file)
        print("✅ Created .env file from template")
        print("🔑 Please edit .env file with your API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️ No .env.sample file found")


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")

    directories = ["audio_output", "output"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")


def main():
    """Main setup function."""
    print("🇫🇷 French Language Tutor - Setup")
    print("=" * 40)

    check_python_version()
    install_dependencies()
    setup_config()
    create_directories()

    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file with your API keys")
    print("2. Run: language-tutor validate")
    print("3. Run: language-tutor run")
    print("\nFor help: language-tutor --help")


if __name__ == "__main__":
    main()
