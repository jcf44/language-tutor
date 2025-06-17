"""Service for handling dialogue operations and LLM interactions."""

from typing import Any, Dict, Optional

from ..api.llm_client import GeminiClient, LLMClient, OpenAIClient
from ..models.config import AppConfig, LLMProvider
from ..models.dialogue import Dialogue


class DialogueService:
    """Service for dialogue generation and management."""

    def __init__(self, config: AppConfig):
        """Initialize the dialogue service with configuration."""
        self.config = config
        self.llm_client = self._create_llm_client()

    def _create_llm_client(self) -> LLMClient:
        """Create appropriate LLM client based on configuration."""
        if self.config.llm_provider == LLMProvider.OPENAI:
            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key is required")
            return OpenAIClient(self.config.openai_api_key)

        elif self.config.llm_provider == LLMProvider.GEMINI:
            if not self.config.gemini_api_key:
                raise ValueError("Gemini API key is required")
            return GeminiClient(self.config.gemini_api_key)

        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.config.llm_provider}"
            )

    async def generate_dialogue(
        self,
        topic: str,
        context: Optional[str] = None,
        level: str = "beginner",
        num_exchanges: Optional[int] = None,
    ) -> Dialogue:
        """Generate a new dialogue on the specified topic."""
        if num_exchanges is None:
            num_exchanges = min(self.config.max_dialogue_length, 8)

        try:
            dialogue = await self.llm_client.generate_dialogue(
                topic=topic,
                context=context,
                level=level,
                num_exchanges=num_exchanges,
            )
            return dialogue

        except Exception as e:
            raise Exception(f"Failed to generate dialogue: {str(e)}")

    async def continue_dialogue(
        self, dialogue: Dialogue, user_input: str
    ) -> str:
        """Continue an existing dialogue with user input."""
        try:
            response = await self.llm_client.continue_dialogue(
                dialogue, user_input
            )
            return response.strip()

        except Exception as e:
            raise Exception(f"Failed to continue dialogue: {str(e)}")

    async def ask_grammar_question(self, question: str) -> str:
        """Ask a grammar question using the LLM client."""
        prompt = (
            "You are a helpful French grammar tutor. "
            "Answer the following grammar question in clear, concise English. "
            "If possible, provide examples.\n\n"
            f"Question: {question}"
        )
        try:
            answer = await self.llm_client.ask_question(prompt)
            return answer
        except Exception as e:
            return f"[Error from LLM: {str(e)}]"

    def validate_dialogue_parameters(
        self, topic: str, level: str, num_exchanges: int
    ) -> Dict[str, Any]:
        """Validate dialogue generation parameters."""
        errors = []

        if not topic or not topic.strip():
            errors.append("Topic cannot be empty")

        if level not in ["beginner", "intermediate", "advanced"]:
            errors.append(
                "Level must be 'beginner', 'intermediate', or 'advanced'"
            )

        if (
            num_exchanges < 1
            or num_exchanges > self.config.max_dialogue_length
        ):
            errors.append(
                f"Number of exchanges must be between 1 and {self.config.max_dialogue_length}"
            )

        return {"valid": len(errors) == 0, "errors": errors}

    def get_dialogue_statistics(self, dialogue: Dialogue) -> Dict[str, Any]:
        """Get statistics about a dialogue."""
        total_messages = len(dialogue.messages)
        user_messages = len(dialogue.get_messages_by_role("user"))
        assistant_messages = len(dialogue.get_messages_by_role("assistant"))

        # Calculate average message length
        if total_messages > 0:
            total_chars = sum(len(msg.content) for msg in dialogue.messages)
            avg_message_length = total_chars / total_messages
        else:
            avg_message_length = 0

        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "average_message_length": round(avg_message_length, 1),
            "level": dialogue.level,
            "topic": dialogue.title,
            "created_at": dialogue.created_at,
            "updated_at": dialogue.updated_at,
        }
