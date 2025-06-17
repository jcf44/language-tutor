"""Service for handling file operations and dialogue import/export."""

import csv
import json
import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd

from ..models.dialogue import Dialogue, DialogueMessage, DialogueRole


class FileService:
    """Service for file operations related to dialogues."""

    def __init__(self, output_directory: str = "output"):
        """Initialize the file service."""
        self.output_directory = output_directory
        os.makedirs(output_directory, exist_ok=True)

    async def import_dialogue_from_text(self, file_path: str) -> Dialogue:
        """Import dialogue from a text file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            return self._parse_text_dialogue(
                content, os.path.basename(file_path)
            )

        except Exception as e:
            raise Exception(f"Error importing dialogue from text: {str(e)}")

    async def import_dialogue_from_markdown(self, file_path: str) -> Dialogue:
        """Import dialogue from a markdown file with enhanced parsing."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            return self._parse_markdown_dialogue(
                content, os.path.basename(file_path)
            )

        except Exception as e:
            raise Exception(
                f"Error importing dialogue from markdown: {str(e)}"
            )

    async def import_dialogue_from_json(self, file_path: str) -> Dialogue:
        """Import dialogue from a JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Handle different JSON formats
            if isinstance(data, dict) and "messages" in data:
                # Structured format
                dialogue = Dialogue(
                    title=data.get("title", "Imported Dialogue"),
                    context=data.get("context"),
                    level=data.get("level", "beginner"),
                )

                for msg_data in data["messages"]:
                    role = DialogueRole(msg_data["role"])
                    content = msg_data["content"]
                    dialogue.add_message(role, content)

                return dialogue

            elif isinstance(data, list):
                # Simple list format
                dialogue = Dialogue(
                    title=os.path.basename(file_path), level="beginner"
                )

                for i, content in enumerate(data):
                    role = (
                        DialogueRole.USER
                        if i % 2 == 0
                        else DialogueRole.ASSISTANT
                    )
                    dialogue.add_message(role, str(content))

                return dialogue

            else:
                raise ValueError("Unsupported JSON format")

        except Exception as e:
            raise Exception(f"Error importing dialogue from JSON: {str(e)}")

    async def import_dialogue_from_csv(self, file_path: str) -> Dialogue:
        """Import dialogue from a CSV file."""
        try:
            df = pd.read_csv(file_path, encoding="utf-8")

            dialogue = Dialogue(
                title=os.path.basename(file_path), level="beginner"
            )

            # Handle different CSV formats
            if "role" in df.columns and "content" in df.columns:
                # Structured CSV with role and content columns
                for _, row in df.iterrows():
                    role = DialogueRole(row["role"])
                    content = str(row["content"])
                    dialogue.add_message(role, content)

            elif len(df.columns) >= 2:
                # Two-column format (speaker, message)
                for _, row in df.iterrows():
                    speaker = str(row.iloc[0]).lower()
                    content = str(row.iloc[1])

                    # Determine role based on speaker
                    if "user" in speaker or "utilisateur" in speaker:
                        role = DialogueRole.USER
                    else:
                        role = DialogueRole.ASSISTANT

                    dialogue.add_message(role, content)

            else:
                raise ValueError("CSV must have at least 2 columns")

            return dialogue

        except Exception as e:
            raise Exception(f"Error importing dialogue from CSV: {str(e)}")

    async def export_dialogue_to_json(
        self, dialogue: Dialogue, filename: Optional[str] = None
    ) -> str:
        """Export dialogue to JSON file."""
        try:
            if not filename:
                filename = f"dialogue_{dialogue.id or 'export'}.json"

            file_path = os.path.join(self.output_directory, filename)

            # Convert dialogue to dictionary
            dialogue_data = {
                "id": dialogue.id,
                "title": dialogue.title,
                "context": dialogue.context,
                "level": dialogue.level,
                "created_at": dialogue.created_at.isoformat(),
                "updated_at": dialogue.updated_at.isoformat()
                if dialogue.updated_at
                else None,
                "messages": [
                    {
                        "role": msg.role.value,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat()
                        if msg.timestamp
                        else None,
                        "audio_file_path": msg.audio_file_path,
                    }
                    for msg in dialogue.messages
                ],
            }

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(dialogue_data, file, ensure_ascii=False, indent=2)

            return file_path

        except Exception as e:
            raise Exception(f"Error exporting dialogue to JSON: {str(e)}")

    async def export_dialogue_to_text(
        self, dialogue: Dialogue, filename: Optional[str] = None
    ) -> str:
        """Export dialogue to text file."""
        try:
            if not filename:
                filename = f"dialogue_{dialogue.id or 'export'}.txt"

            file_path = os.path.join(self.output_directory, filename)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(dialogue.to_text())

            return file_path

        except Exception as e:
            raise Exception(f"Error exporting dialogue to text: {str(e)}")

    def _parse_text_dialogue(self, content: str, filename: str) -> Dialogue:
        """Parse text content into a Dialogue object."""
        dialogue = Dialogue(title=filename, level="beginner")

        lines = content.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for speaker patterns
            if ":" in line:
                speaker, message = line.split(":", 1)
                speaker = speaker.strip().lower()
                message = message.strip()

                # Determine role based on speaker indicators
                if any(
                    word in speaker
                    for word in ["user", "utilisateur", "client", "étudiant"]
                ):
                    role = DialogueRole.USER
                elif any(
                    word in speaker
                    for word in ["assistant", "tuteur", "prof", "teacher"]
                ):
                    role = DialogueRole.ASSISTANT
                else:
                    # Alternate between user and assistant
                    last_role = (
                        dialogue.messages[-1].role
                        if dialogue.messages
                        else DialogueRole.ASSISTANT
                    )
                    role = (
                        DialogueRole.USER
                        if last_role == DialogueRole.ASSISTANT
                        else DialogueRole.ASSISTANT
                    )

                dialogue.add_message(role, message)

            else:
                # If no speaker indicated, alternate roles
                last_role = (
                    dialogue.messages[-1].role
                    if dialogue.messages
                    else DialogueRole.ASSISTANT
                )
                role = (
                    DialogueRole.USER
                    if last_role == DialogueRole.ASSISTANT
                    else DialogueRole.ASSISTANT
                )
                dialogue.add_message(role, line)

        return dialogue

    def _parse_markdown_dialogue(
        self, content: str, filename: str
    ) -> Dialogue:
        """Parse markdown content into a Dialogue object with enhanced formatting support."""
        # Extract title from first # heading if present
        title_match = re.match(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename

        # Extract level from metadata if present
        level_match = re.search(
            r"\*\*(?:Level|Niveau):\*\*\s*(\w+)", content, re.IGNORECASE
        )
        level = level_match.group(1).lower() if level_match else "beginner"

        # Extract context from metadata if present
        context_match = re.search(
            r"\*\*(?:Context|Contexte):\*\*\s*(.+?)(?:\n\n|\n---|\Z)",
            content,
            re.IGNORECASE | re.DOTALL,
        )
        context = context_match.group(1).strip() if context_match else None

        dialogue = Dialogue(title=title, level=level, context=context)

        # Split content into lines and process
        lines = content.split("\n")

        for line in lines:
            line = line.strip()

            # Skip empty lines, headers, metadata, and separators
            if (
                not line
                or line.startswith("#")
                or line.startswith("---")
                or ("level:" in line.lower() and "**" in line)
                or ("context:" in line.lower() and "**" in line)
            ):
                continue

            # Handle markdown speaker format: **Speaker:** or *Speaker:*
            speaker_match = re.match(r"\*{1,2}(.+?):\*{1,2}\s*(.+)", line)
            if speaker_match:
                speaker = speaker_match.group(1).strip().lower()
                message = speaker_match.group(2).strip()
            elif ":" in line:
                # Handle regular speaker format: Speaker: message
                speaker, message = line.split(":", 1)
                speaker = speaker.strip().lower()
                message = message.strip()
            else:
                # No speaker format, skip this line
                continue

            # Clean up markdown formatting from message
            if message:
                # Remove markdown formatting but keep the text
                message = re.sub(
                    r"\*{1,2}(.+?)\*{1,2}", r"\1", message
                )  # Bold/italic
                message = re.sub(r"`(.+?)`", r"\1", message)  # Code
                message = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", message)  # Links

                # Determine speaker role
                if speaker:
                    if any(
                        word in speaker
                        for word in [
                            "user",
                            "utilisateur",
                            "client",
                            "étudiant",
                            "student",
                        ]
                    ):
                        role = DialogueRole.USER
                    elif any(
                        word in speaker
                        for word in [
                            "assistant",
                            "tuteur",
                            "prof",
                            "teacher",
                            "tutor",
                        ]
                    ):
                        role = DialogueRole.ASSISTANT
                    else:
                        # Default alternating
                        last_role = (
                            dialogue.messages[-1].role
                            if dialogue.messages
                            else DialogueRole.ASSISTANT
                        )
                        role = (
                            DialogueRole.USER
                            if last_role == DialogueRole.ASSISTANT
                            else DialogueRole.ASSISTANT
                        )

                    dialogue.add_message(role, message)

        return dialogue

    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return [".txt", ".json", ".csv", ".md"]

    def validate_file_format(self, file_path: str) -> bool:
        """Validate if file format is supported."""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.get_supported_formats()
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.get_supported_formats()
