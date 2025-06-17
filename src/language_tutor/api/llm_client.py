"""LLM client implementations for dialogue generation."""

import asyncio
from abc import ABC, abstractmethod
from typing import List, Optional

import google.generativeai as genai
import openai

from ..models.dialogue import Dialogue, DialogueMessage, DialogueRole


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def generate_dialogue(
        self,
        topic: str,
        context: Optional[str] = None,
        level: str = "beginner",
        num_exchanges: int = 5,
    ) -> Dialogue:
        """Generate a dialogue based on the given parameters."""
        pass

    @abstractmethod
    async def continue_dialogue(
        self, dialogue: Dialogue, user_input: str
    ) -> str:
        """Continue an existing dialogue with user input."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI GPT client for dialogue generation."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the OpenAI client."""
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_dialogue(
        self,
        topic: str,
        context: Optional[str] = None,
        level: str = "beginner",
        num_exchanges: int = 5,
    ) -> Dialogue:
        """Generate a dialogue using OpenAI GPT."""
        # Create system prompt
        system_prompt = self._create_system_prompt(level, context)

        # Create user prompt
        user_prompt = f"""Créez un dialogue en français sur le sujet: {topic}
        
Le dialogue doit contenir {num_exchanges} échanges entre deux personnes.
Formatez la réponse comme suit:

Personne A: [message]
Personne B: [message]
Personne A: [message]
Personne B: [message]
...

Le dialogue doit être naturel et approprié pour le niveau {level}."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            # Parse the response and create dialogue
            dialogue_text = response.choices[0].message.content
            return self._parse_dialogue_response(
                dialogue_text, topic, context, level
            )

        except Exception as e:
            raise Exception(f"Error generating dialogue with OpenAI: {str(e)}")

    async def continue_dialogue(
        self, dialogue: Dialogue, user_input: str
    ) -> str:
        """Continue an existing dialogue with user input."""
        # Prepare conversation history
        messages = [
            {
                "role": "system",
                "content": self._create_system_prompt(
                    dialogue.level, dialogue.context
                ),
            }
        ]

        # Add dialogue history
        for msg in dialogue.messages[-6:]:  # Last 6 messages for context
            role = "user" if msg.role == DialogueRole.USER else "assistant"
            messages.append({"role": role, "content": msg.content})

        # Add new user input
        messages.append({"role": "user", "content": user_input})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error continuing dialogue with OpenAI: {str(e)}")

    def _create_system_prompt(
        self, level: str, context: Optional[str] = None
    ) -> str:
        """Create system prompt for dialogue generation."""
        base_prompt = f"""Vous êtes un tuteur de français expérimenté. Votre rôle est de créer et participer à des dialogues en français naturel et authentique.

Niveau: {level}
- beginner: Utilisez un vocabulaire simple, des phrases courtes, des structures grammaticales de base
- intermediate: Utilisez un vocabulaire plus varié, des phrases de complexité moyenne
- advanced: Utilisez un vocabulaire riche, des expressions idiomatiques, des structures complexes

Règles importantes:
1. Répondez UNIQUEMENT en français
2. Adaptez le vocabulaire et la complexité au niveau spécifié
3. Utilisez des expressions naturelles et authentiques
4. Corrigez subtilement les erreurs si nécessaire
5. Encouragez la conversation"""

        if context:
            base_prompt += f"\n\nContexte du dialogue: {context}"

        return base_prompt

    def _parse_dialogue_response(
        self,
        dialogue_text: str,
        topic: str,
        context: Optional[str],
        level: str,
    ) -> Dialogue:
        """Parse OpenAI response into Dialogue object."""
        dialogue = Dialogue(title=topic, context=context, level=level)

        lines = dialogue_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if ":" in line:
                speaker, content = line.split(":", 1)
                content = content.strip()

                # Determine role based on speaker
                role = (
                    DialogueRole.USER
                    if "A" in speaker
                    else DialogueRole.ASSISTANT
                )
                dialogue.add_message(role, content)

        return dialogue


class GeminiClient(LLMClient):
    """Google Gemini client for dialogue generation."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """Initialize the Gemini client."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    async def generate_dialogue(
        self,
        topic: str,
        context: Optional[str] = None,
        level: str = "beginner",
        num_exchanges: int = 5,
    ) -> Dialogue:
        """Generate a dialogue using Google Gemini."""
        system_prompt = self._create_system_prompt(level, context)

        user_prompt = f"""Créez un dialogue en français sur le sujet: {topic}
        
Le dialogue doit contenir {num_exchanges} échanges entre deux personnes.
Formatez la réponse comme suit:

Personne A: [message]
Personne B: [message]
Personne A: [message]
Personne B: [message]
...

Le dialogue doit être naturel et approprié pour le niveau {level}."""

        try:
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            response = await asyncio.get_event_loop().run_in_executor(
                None, self.model.generate_content, full_prompt
            )

            dialogue_text = response.text
            return self._parse_dialogue_response(
                dialogue_text, topic, context, level
            )

        except Exception as e:
            raise Exception(f"Error generating dialogue with Gemini: {str(e)}")

    async def continue_dialogue(
        self, dialogue: Dialogue, user_input: str
    ) -> str:
        """Continue an existing dialogue with user input."""
        system_prompt = self._create_system_prompt(
            dialogue.level, dialogue.context
        )

        # Build conversation context
        conversation_history = ""
        for msg in dialogue.messages[-6:]:  # Last 6 messages for context
            speaker = (
                "Utilisateur" if msg.role == DialogueRole.USER else "Assistant"
            )
            conversation_history += f"{speaker}: {msg.content}\n"

        full_prompt = f"""{system_prompt}

Historique de la conversation:
{conversation_history}

Nouvelle entrée de l'utilisateur: {user_input}

Répondez naturellement en français pour continuer la conversation."""

        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.model.generate_content, full_prompt
            )

            return response.text

        except Exception as e:
            raise Exception(f"Error continuing dialogue with Gemini: {str(e)}")

    def _create_system_prompt(
        self, level: str, context: Optional[str] = None
    ) -> str:
        """Create system prompt for dialogue generation."""
        base_prompt = f"""Vous êtes un tuteur de français expérimenté. Votre rôle est de créer et participer à des dialogues en français naturel et authentique.

Niveau: {level}
- beginner: Utilisez un vocabulaire simple, des phrases courtes, des structures grammaticales de base
- intermediate: Utilisez un vocabulaire plus varié, des phrases de complexité moyenne
- advanced: Utilisez un vocabulaire riche, des expressions idiomatiques, des structures complexes

Règles importantes:
1. Répondez UNIQUEMENT en français
2. Adaptez le vocabulaire et la complexité au niveau spécifié
3. Utilisez des expressions naturelles et authentiques
4. Corrigez subtilement les erreurs si nécessaire
5. Encouragez la conversation"""

        if context:
            base_prompt += f"\n\nContexte du dialogue: {context}"

        return base_prompt

    def _parse_dialogue_response(
        self,
        dialogue_text: str,
        topic: str,
        context: Optional[str],
        level: str,
    ) -> Dialogue:
        """Parse Gemini response into Dialogue object."""
        dialogue = Dialogue(title=topic, context=context, level=level)

        lines = dialogue_text.strip().split("\n")
        for line in lines:
            line = line.strip()
            if ":" in line:
                speaker, content = line.split(":", 1)
                content = content.strip()

                # Determine role based on speaker
                role = (
                    DialogueRole.USER
                    if "A" in speaker
                    else DialogueRole.ASSISTANT
                )
                dialogue.add_message(role, content)

        return dialogue

        return dialogue
