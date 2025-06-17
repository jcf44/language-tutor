"""Dialogue models for the language tutor application."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DialogueRole(str, Enum):
    """Dialogue participant roles."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class DialogueMessage(BaseModel):
    """A single message in a dialogue."""

    role: DialogueRole
    content: str = Field(description="The message content in French")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    audio_file_path: Optional[str] = Field(
        default=None, description="Path to generated audio file"
    )


class Dialogue(BaseModel):
    """A complete dialogue conversation."""

    id: Optional[str] = Field(default=None)
    title: str = Field(description="Dialogue title or topic")
    context: Optional[str] = Field(
        default=None, description="Context or scenario for the dialogue"
    )
    level: str = Field(
        default="beginner",
        description="Difficulty level (beginner, intermediate, advanced)",
    )
    messages: List[DialogueMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    def add_message(self, role: DialogueRole, content: str) -> None:
        """Add a message to the dialogue."""
        message = DialogueMessage(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_by_role(
        self, role: DialogueRole
    ) -> List[DialogueMessage]:
        """Get all messages from a specific role."""
        return [msg for msg in self.messages if msg.role == role]

    def to_text(self) -> str:
        """Convert dialogue to plain text format."""
        text_lines = [f"Title: {self.title}"]
        if self.context:
            text_lines.append(f"Context: {self.context}")
        text_lines.append(f"Level: {self.level}")
        text_lines.append("")

        for msg in self.messages:
            speaker = (
                "Utilisateur" if msg.role == DialogueRole.USER else "Assistant"
            )
            text_lines.append(f"{speaker}: {msg.content}")

        return "\n".join(text_lines)
        return "\n".join(text_lines)
