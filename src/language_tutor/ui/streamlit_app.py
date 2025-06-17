"""Streamlit web interface for the French Language Tutor."""

import asyncio
import os
import sys
import tempfile
from typing import Any, Dict, Optional

import streamlit as st

# Set page config as the very first Streamlit command
st.set_page_config(
    page_title="French Language Tutor", page_icon="🇫🇷", layout="wide"
)

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from language_tutor.config_manager import config_manager
from language_tutor.models.dialogue import Dialogue, DialogueRole
from language_tutor.services.audio_service import AudioService
from language_tutor.services.dialogue_service import DialogueService
from language_tutor.services.file_service import FileService
from language_tutor.services.stt_service import STTService


class LanguageTutorUI:
    """Main UI class for the Language Tutor application."""

    def __init__(self):
        """Initialize the UI."""
        self.config = None
        self.dialogue_service = None
        self.file_service = None
        self.audio_service = None
        self.stt_service = None
        self._initialize_services()

    def _initialize_services(self):
        """Initialize services with configuration."""
        self.config = config_manager.load_config()
        config_manager.validate_config(self.config)

        self.dialogue_service = DialogueService(self.config)
        self.file_service = FileService()
        self.audio_service = AudioService(self.config)
        self.stt_service = STTService(self.config)

    def run(self):
        """Run the Streamlit application."""
        st.title("🇫🇷 French Language Tutor")
        st.markdown(
            "*Practice French through AI-generated dialogues with high-quality audio*"
        )

        # Sidebar for configuration and options
        self._render_sidebar()

        # Main content area
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Generate Dialogue",
                "Import Dialogue",
                "Practice Mode",
                "Audio Library",
                "Grammar Help",
            ]
        )

        with tab1:
            self._render_generate_dialogue_tab()

        with tab2:
            self._render_import_dialogue_tab()

        with tab3:
            self._render_practice_mode_tab()

        with tab4:
            self._render_audio_library_tab()

        with tab5:
            self._render_grammar_tab()

    def _render_sidebar(self):
        """Render the sidebar with configuration options."""
        st.sidebar.header("⚙️ Configuration")

        # Display current configuration
        st.sidebar.markdown(
            f"**LLM Provider:** {self.config.llm_provider.value}"
        )
        st.sidebar.markdown(
            f"**TTS Provider:** {self.config.tts_provider.value}"
        )

        # Voice selection
        if st.sidebar.button("🔊 Get Available Voices"):
            with st.sidebar.container():
                with st.spinner("Loading available voices..."):
                    try:
                        voices = asyncio.run(
                            self.audio_service.get_available_voices()
                        )
                        st.session_state.available_voices = voices
                        st.sidebar.success(f"Found {len(voices)} voices")
                    except Exception as e:
                        st.sidebar.error(f"Error loading voices: {str(e)}")

        # Display available voices
        if "available_voices" in st.session_state:
            selected_voice = st.sidebar.selectbox(
                "Select Voice",
                options=st.session_state.available_voices,
                key="selected_voice",
            )

        st.sidebar.markdown("---")

        # Help section
        with st.sidebar.expander("ℹ️ Help"):
            st.markdown("""
            **How to use:**
            1. **Generate**: Create new dialogues with AI
            2. **Import**: Upload your own dialogue files
            3. **Practice**: Interactive conversation mode
            4. **Audio**: Download generated audio files
            
            **Supported formats:** TXT, JSON, CSV, MD
            """)

    def _render_generate_dialogue_tab(self):
        """Render the dialogue generation tab."""
        st.header("🤖 Generate New Dialogue")

        col1, col2 = st.columns([2, 1])

        with col1:
            topic = st.text_input(
                "Dialogue Topic",
                placeholder="e.g., Ordering food at a restaurant",
                help="Enter a topic or scenario for the dialogue",
            )

            context = st.text_area(
                "Additional Context (Optional)",
                placeholder="e.g., A tourist in Paris wants to order lunch",
                help="Provide additional context to make the dialogue more specific",
            )

        with col2:
            level = st.selectbox(
                "Difficulty Level",
                options=["beginner", "intermediate", "advanced"],
                help="Choose the appropriate difficulty level",
            )

            num_exchanges = st.number_input(
                "Number of Exchanges",
                min_value=2,
                max_value=self.config.max_dialogue_length,
                value=5,
                help="Number of back-and-forth exchanges in the dialogue",
            )

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            generate_button = st.button("🚀 Generate Dialogue", type="primary")

        with col2:
            generate_audio = st.checkbox("Generate Audio", value=True)

        if generate_button and topic:
            with st.spinner("Generating dialogue..."):
                try:
                    # Generate dialogue
                    dialogue = asyncio.run(
                        self.dialogue_service.generate_dialogue(
                            topic=topic,
                            context=context,
                            level=level,
                            num_exchanges=num_exchanges,
                        )
                    )

                    # Store dialogue in session state
                    st.session_state.current_dialogue = dialogue

                    # Generate audio if requested
                    if generate_audio:
                        with st.spinner("Generating audio..."):
                            dialogue = asyncio.run(
                                self.audio_service.generate_audio_for_dialogue(
                                    dialogue
                                )
                            )
                            st.session_state.current_dialogue = dialogue

                    st.success("Dialogue generated successfully!")

                except Exception as e:
                    st.error(f"Error generating dialogue: {str(e)}")

        # Display generated dialogue
        if "current_dialogue" in st.session_state:
            self._display_dialogue(st.session_state.current_dialogue)

    def _render_import_dialogue_tab(self):
        """Render the dialogue import tab."""
        st.header("📁 Import Dialogue")

        # File upload
        uploaded_file = st.file_uploader(
            "Choose a dialogue file",
            type=["txt", "json", "csv", "md"],
            help="Upload a dialogue file in supported format",
        )

        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}"
            ) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            try:
                # Import dialogue based on file extension
                file_ext = uploaded_file.name.split(".")[-1].lower()

                with st.spinner("Importing dialogue..."):
                    if file_ext == "json":
                        dialogue = asyncio.run(
                            self.file_service.import_dialogue_from_json(
                                tmp_path
                            )
                        )
                    elif file_ext == "csv":
                        dialogue = asyncio.run(
                            self.file_service.import_dialogue_from_csv(
                                tmp_path
                            )
                        )
                    elif file_ext == "md":
                        dialogue = asyncio.run(
                            self.file_service.import_dialogue_from_markdown(
                                tmp_path
                            )
                        )
                    else:  # txt
                        dialogue = asyncio.run(
                            self.file_service.import_dialogue_from_text(
                                tmp_path
                            )
                        )

                # Store dialogue in session state
                st.session_state.imported_dialogue = dialogue
                st.success("Dialogue imported successfully!")

                # Option to generate audio
                if st.button("🔊 Generate Audio for Imported Dialogue"):
                    with st.spinner("Generating audio..."):
                        dialogue = asyncio.run(
                            self.audio_service.generate_audio_for_dialogue(
                                dialogue
                            )
                        )
                        st.session_state.imported_dialogue = dialogue
                        st.success("Audio generated!")

            except Exception as e:
                st.error(f"Error importing dialogue: {str(e)}")

            finally:
                # Clean up temporary file
                os.unlink(tmp_path)

        # Display imported dialogue
        if "imported_dialogue" in st.session_state:
            self._display_dialogue(st.session_state.imported_dialogue)

    def _render_practice_mode_tab(self):
        """Render the interactive practice mode tab."""
        st.header("💬 Practice Mode")
        try:
            # Initialize practice dialogue if not exists
            if "practice_dialogue" not in st.session_state:
                st.session_state.practice_dialogue = None
                st.session_state.practice_messages = []

            # Start new practice session
            col1, col2 = st.columns([3, 1])

            with col1:
                practice_topic = st.text_input(
                    "Practice Topic", placeholder="e.g., Asking for directions"
                )

            with col2:
                practice_level = st.selectbox(
                    "Level",
                    options=["beginner", "intermediate", "advanced"],
                    key="practice_level",
                )

            if st.button("🎯 Start Practice Session") and practice_topic:
                try:
                    st.write("[DEBUG] Creating Dialogue object...")
                    st.session_state.practice_dialogue = Dialogue(
                        title=practice_topic, level=practice_level
                    )
                    st.session_state.practice_messages = []
                    st.success(
                        "Practice session started! Type your first message below."
                    )
                except Exception as e:
                    st.error(f"❌ Failed to start practice session: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    print("[PracticeMode] Dialogue creation error:", e)
                    return

            # Practice interface
            if st.session_state.practice_dialogue:
                st.markdown("---")

                # Voice input instructions
                with st.expander("🎤 Voice Input Help"):
                    st.markdown("""
                    **How to use voice input:**
                    1. Click "🔧 Test Mic" to check your microphone
                    2. Click "🎤 Record" and speak clearly in French
                    3. The app will listen for 10 seconds maximum
                    4. Your speech will be converted to text automatically
                    
                    **Tips for best results:**
                    - Speak clearly and at normal speed
                    - Minimize background noise
                    - Grant microphone permissions when prompted
                    - Use French pronunciation
                    """)

                # Display conversation history
                for msg in st.session_state.practice_messages:
                    if msg["role"] == "user":
                        st.chat_message("user").write(msg["content"])
                    else:
                        with st.chat_message("assistant"):
                            st.write(msg["content"])
                            if "audio_path" in msg and msg["audio_path"]:
                                st.audio(msg["audio_path"])

                # --- Robust input processing: use a flag to trigger processing ---
                if "practice_input_to_process" not in st.session_state:
                    st.session_state.practice_input_to_process = False

                # If flag is set, process input, clear input and flag, then return
                if st.session_state.practice_input_to_process:
                    user_input = st.session_state.practice_text_input
                    last_user_msg = next((m for m in reversed(st.session_state.practice_messages) if m["role"] == "user"), None)
                    if user_input and (not last_user_msg or last_user_msg["content"] != user_input):
                        try:
                            st.session_state.practice_messages.append({"role": "user", "content": user_input})
                            st.session_state.practice_dialogue.add_message(DialogueRole.USER, user_input)
                            with st.spinner("Generating response..."):
                                try:
                                    if self.dialogue_service:
                                        response = asyncio.run(
                                            self.dialogue_service.continue_dialogue(
                                                st.session_state.practice_dialogue, user_input
                                            )
                                        )
                                    else:
                                        response = "Service not available. Please refresh and try again."
                                    st.session_state.practice_dialogue.add_message(DialogueRole.ASSISTANT, response)
                                    audio_path = None
                                    if self.audio_service:
                                        try:
                                            audio_path = asyncio.run(
                                                self.audio_service.create_temporary_audio(response)
                                            )
                                        except Exception as audio_e:
                                            st.warning(f"Could not generate audio: {str(audio_e)}")
                                    st.session_state.practice_messages.append({
                                        "role": "assistant",
                                        "content": response,
                                        "audio_path": audio_path,
                                    })
                                except Exception as dialogue_e:
                                    st.error(f"Error generating response: {str(dialogue_e)}")
                                    st.info("💡 Please try again or refresh the page.")
                        except Exception as input_e:
                            st.error(f"Error processing input: {str(input_e)}")
                            st.info("💡 Please try again.")
                    # Clear input and flag before rerun
                    st.session_state.practice_text_input = ""
                    st.session_state.practice_input_to_process = False
                    st.rerun()
                    return

                # --- Handle voice input result before rendering widget ---
                if "practice_voice_result" in st.session_state and st.session_state.practice_voice_result:
                    st.session_state.practice_text_input = st.session_state.practice_voice_result
                    st.session_state.practice_input_to_process = True
                    st.session_state.practice_voice_result = ""
                    st.rerun()
                    return

                # User input options
                st.markdown("#### 💬 Your Response")
                col1, col2 = st.columns([4, 1])
                with col1:
                    user_input = st.text_input(
                        "Type your message in French:",
                        key="practice_text_input",
                        placeholder="Tapez votre message ici...",
                    )
                    # If user presses enter or submits, set flag to process input
                    if user_input and st.session_state.practice_text_input == user_input and st.session_state.practice_input_to_process is False:
                        st.session_state.practice_input_to_process = True
                        st.rerun()
                        return
                with col2:
                    st.markdown("**Or use voice:**")
                    # Microphone test button
                    if st.button(
                        "🔧 Test Mic",
                        key="test_mic_btn",
                        help="Test your microphone",
                    ):
                        if hasattr(self, "stt_service"):
                            try:
                                mic_works, message = (
                                    self.stt_service.test_microphone()
                                )
                                if mic_works:
                                    st.success(f"🎤 {message}")
                                else:
                                    st.error(f"❌ {message}")
                            except Exception as e:
                                st.error(f"Microphone test failed: {str(e)}")
                        else:
                            st.error("STT service not available")
                    # Voice record button
                    if st.button(
                        "🎤 Record",
                        key="voice_record_btn",
                        help="Click and speak in French",
                    ):
                        if hasattr(self, "stt_service"):
                            with st.spinner("🎧 Listening... Speak now!"):
                                try:
                                    voice_text = asyncio.run(
                                        self.stt_service.listen_for_speech(
                                            timeout=3,
                                            phrase_time_limit=10,
                                            language="fr-FR",
                                        )
                                    )
                                    if voice_text:
                                        st.success(f"Heard: {voice_text}")
                                        st.session_state.practice_voice_result = voice_text
                                        st.rerun()
                                        return
                                    else:
                                        st.warning(
                                            "No speech detected. Try again."
                                        )
                                except Exception as e:
                                    st.error(f"Speech error: {str(e)}")
                                    st.info("💡 Make sure your microphone works.")
                        else:
                            st.error("Speech recognition not available.")

        except Exception as e:
            st.error(f"❌ Practice Mode crashed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            print("[PracticeMode] Tab error:", e)
            return

    def _render_audio_library_tab(self):
        """Render the audio library tab."""
        st.header("🎵 Audio Library")

        # Show audio files for current dialogues
        dialogues_to_show = []

        if "current_dialogue" in st.session_state:
            dialogues_to_show.append(
                ("Generated Dialogue", st.session_state.current_dialogue)
            )

        if "imported_dialogue" in st.session_state:
            dialogues_to_show.append(
                ("Imported Dialogue", st.session_state.imported_dialogue)
            )

        if not dialogues_to_show:
            st.info(
                "No dialogues with audio available. Generate or import a dialogue first."
            )
            return

        for dialogue_name, dialogue in dialogues_to_show:
            with st.expander(f"🎤 {dialogue_name}: {dialogue.title}"):
                st.markdown(f"**Level:** {dialogue.level}")
                st.markdown(f"**Messages:** {len(dialogue.messages)}")

                # Individual message audio
                for i, message in enumerate(dialogue.messages):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        speaker = (
                            "👤 User"
                            if message.role == DialogueRole.USER
                            else "🤖 Assistant"
                        )
                        st.markdown(f"**{speaker}:** {message.content}")

                    with col2:
                        if message.audio_file_path and os.path.exists(
                            message.audio_file_path
                        ):
                            st.audio(message.audio_file_path)
                        else:
                            if st.button(
                                f"🔊 Generate",
                                key=f"audio_{dialogue_name}_{i}",
                            ):
                                with st.spinner("Generating audio..."):
                                    try:
                                        audio_path = asyncio.run(
                                            self.audio_service.generate_audio_for_text(
                                                message.content,
                                                filename=f"msg_{i}.mp3",
                                            )
                                        )
                                        message.audio_file_path = audio_path
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")

                # Complete dialogue audio
                st.markdown("---")
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button(
                        f"🎵 Generate Complete Audio",
                        key=f"complete_{dialogue_name}",
                    ):
                        with st.spinner(
                            "Generating complete dialogue audio..."
                        ):
                            try:
                                audio_path = asyncio.run(
                                    self.audio_service.generate_complete_dialogue_audio(
                                        dialogue,
                                        filename=f"complete_{dialogue.title.replace(' ', '_')}.mp3",
                                    )
                                )
                                st.success("Complete audio generated!")
                                st.audio(audio_path)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                with col2:
                    # Export options
                    export_format = st.selectbox(
                        "Export Format",
                        options=["JSON", "Text"],
                        key=f"export_format_{dialogue_name}",
                    )

                    if st.button(f"📥 Export", key=f"export_{dialogue_name}"):
                        try:
                            if export_format == "JSON":
                                file_path = asyncio.run(
                                    self.file_service.export_dialogue_to_json(
                                        dialogue
                                    )
                                )
                            else:
                                file_path = asyncio.run(
                                    self.file_service.export_dialogue_to_text(
                                        dialogue
                                    )
                                )

                            st.success(f"Exported to: {file_path}")

                        except Exception as e:
                            st.error(f"Export error: {str(e)}")

    def _render_grammar_tab(self):
        """Render the Grammar tab with chat-like UI for questions and rules."""
        st.header("📚 Grammar Help")
        st.markdown("Ask a grammar question or explore common French grammar rules.")

        # --- Grammar Question Chat ---
        st.subheader("Ask a Grammar Question")
        if "grammar_chat" not in st.session_state:
            st.session_state.grammar_chat = []
        # --- Robust input processing for grammar question ---
        if "grammar_question_to_process" not in st.session_state:
            st.session_state.grammar_question_to_process = False
        if st.session_state.grammar_question_to_process:
            grammar_question = st.session_state.grammar_question_input
            if grammar_question:
                answer = self._answer_grammar_question(grammar_question)
                st.session_state.grammar_chat.append({"role": "user", "content": grammar_question})
                st.session_state.grammar_chat.append({"role": "assistant", "content": answer})
            st.session_state.grammar_question_input = ""
            st.session_state.grammar_question_to_process = False
            st.rerun()
            return

        grammar_question = st.text_input("Type your grammar question:", key="grammar_question_input", placeholder="e.g., When do I use 'le' vs 'la'?")
        if st.button("Ask Grammar Question") and grammar_question:
            st.session_state.grammar_question_to_process = True
            st.rerun()
            return
        # Display chat
        for msg in st.session_state.grammar_chat:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

        st.markdown("---")
        # --- Grammar Rules List ---
        st.subheader("Most Used Grammar Rules")
        grammar_rules = [
            {"title": "Gender of Nouns (le/la)", "doc": "In French, nouns are either masculine (le) or feminine (la). For example: le livre (the book), la table (the table)."},
            {"title": "Verb Conjugation: Être & Avoir", "doc": "Être (to be) and Avoir (to have) are the two most important verbs. Example: Je suis (I am), Tu as (You have)."},
            {"title": "Adjective Agreement", "doc": "Adjectives must agree in gender and number with the noun. Example: un livre intéressant, une table intéressante."},
            {"title": "Negation (ne...pas)", "doc": "To make a sentence negative, wrap the verb with ne...pas. Example: Je ne parle pas français."},
            {"title": "Question Formation", "doc": "You can ask questions by inverting subject and verb, or using 'est-ce que'. Example: Parlez-vous français ? / Est-ce que vous parlez français ?"},
            {"title": "Definite & Indefinite Articles", "doc": "le, la, les (the); un, une, des (a, an, some)."},
            {"title": "Prepositions of Place", "doc": "à (at), dans (in), sur (on), sous (under), devant (in front of), derrière (behind)."},
            {"title": "Possessive Adjectives", "doc": "mon, ma, mes (my); ton, ta, tes (your); son, sa, ses (his/her)."},
            {"title": "Reflexive Verbs", "doc": "Verbs used with 'se' (oneself). Example: se laver (to wash oneself)."},
            {"title": "Past Tense: Passé Composé", "doc": "Formed with être or avoir + past participle. Example: J'ai mangé (I ate), Je suis allé(e) (I went)."},
            {"title": "Future Tense: Futur Proche", "doc": "Formed with aller + infinitive. Example: Je vais manger (I am going to eat)."},
            {"title": "Direct & Indirect Objects", "doc": "me, te, le, la, nous, vous, les (direct); lui, leur (indirect)."},
            {"title": "Impersonal Expressions", "doc": "Il faut (it is necessary), Il y a (there is/are)."},
            {"title": "Demonstrative Adjectives", "doc": "ce, cet, cette, ces (this/that/these/those)."},
            {"title": "Relative Pronouns", "doc": "qui, que, où (who, that, where)."},
            {"title": "Imperative Mood", "doc": "Used for commands. Example: Parle! (Speak!), Finissez! (Finish!)"},
            {"title": "Partitive Articles", "doc": "du, de la, de l', des (some/any)."},
            {"title": "Numbers & Counting", "doc": "un, deux, trois...; premier, deuxième... (first, second...)."},
            {"title": "Time Expressions", "doc": "aujourd'hui (today), demain (tomorrow), hier (yesterday)."},
            {"title": "Common Irregular Verbs", "doc": "aller, faire, venir, pouvoir, vouloir, devoir, etc."},
        ]
        if "grammar_rule_chat" not in st.session_state:
            st.session_state.grammar_rule_chat = []
        # Organize buttons in 3 columns
        cols = st.columns(3)
        for i, rule in enumerate(grammar_rules):
            col = cols[i % 3]
            if col.button(rule["title"], key=f"grammar_rule_{i}"):
                st.session_state.grammar_rule_chat.append({"role": "user", "content": rule["title"]})
                answer = self._answer_grammar_question(rule["title"])
                st.session_state.grammar_rule_chat.append({"role": "assistant", "content": answer})
                st.rerun()
                return
        # Display rule chat
        for msg in st.session_state.grammar_rule_chat:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

    def _answer_grammar_question(self, question):
        # Use the LLM via DialogueService to answer grammar questions
        try:
            import asyncio
            answer = asyncio.run(self.dialogue_service.ask_grammar_question(question))
            return answer
        except Exception as e:
            return f"[Error: {str(e)}]"

    def _display_dialogue(self, dialogue: Dialogue):
        """Display a dialogue in a formatted way."""
        st.markdown("---")

        # Dialogue info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Level", dialogue.level.title())
        with col2:
            st.metric("Messages", len(dialogue.messages))
        with col3:
            if dialogue.created_at:
                st.metric("Created", dialogue.created_at.strftime("%H:%M"))

        # Display messages
        st.markdown("### 💬 Dialogue")

        for i, message in enumerate(dialogue.messages):
            if message.role == DialogueRole.USER:
                with st.chat_message("user"):
                    st.write(message.content)
                    if message.audio_file_path and os.path.exists(
                        message.audio_file_path
                    ):
                        st.audio(message.audio_file_path)
            else:
                with st.chat_message("assistant"):
                    st.write(message.content)
                    if message.audio_file_path and os.path.exists(
                        message.audio_file_path
                    ):
                        st.audio(message.audio_file_path)


def main():
    """Main entry point for the Streamlit app."""
    try:
        ui = LanguageTutorUI()
        ui.run()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()
