"""French Practice AI Application - Language Tutor."""

from .config_manager import ConfigManager
from .models import AppConfig, Dialogue, DialogueRole
from .services import AudioService, DialogueService, FileService

__version__ = "0.1.0"
__all__ = [
    "ConfigManager",
    "Dialogue",
    "DialogueRole",
    "AppConfig",
    "DialogueService",
    "FileService",
    "AudioService",
]
