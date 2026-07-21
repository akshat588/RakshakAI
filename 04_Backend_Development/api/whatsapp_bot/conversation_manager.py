"""
RakshakAI v2
WhatsApp Conversation Manager

Handles conversation state, onboarding, preferred language,
and user interaction flow.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, Optional

from api.user_management.preferences import preferences
from .bot_config import bot_config


class ConversationManager:
    """
    Manages WhatsApp conversations.
    """

    def __init__(self) -> None:

        self.preferences = preferences

        self.sessions: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Session
    # ==========================================================

    def get_session(
        self,
        phone_number: str,
    ) -> Dict[str, Any]:

        if phone_number not in self.sessions:

            self.sessions[phone_number] = {
                "phone_number": phone_number,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "last_activity": datetime.utcnow().isoformat() + "Z",
                "onboarding_completed": False,
                "awaiting_language": True,
                "current_state": "language_selection",
            }

        return self.sessions[phone_number]

    # ==========================================================
    # Check Onboarding
    # ==========================================================

    def requires_onboarding(
        self,
        phone_number: str,
    ) -> bool:

        user_preferences = self.preferences.get(phone_number)

        if user_preferences.get("preferred_language"):
            return False

        session = self.get_session(phone_number)

        return not session["onboarding_completed"]

    # ==========================================================
    # Language Selection
    # ==========================================================

    def save_language(
        self,
        phone_number: str,
        language_input: str,
    ) -> Optional[str]:

        language_input = language_input.strip()

        language = None

        if language_input in bot_config.SUPPORTED_LANGUAGES:

            language = bot_config.SUPPORTED_LANGUAGES[language_input]

        else:

            language = bot_config.LANGUAGE_ALIASES.get(language_input.lower())

        if language is None:

            return None

        self.preferences.update(
            phone_number,
            {
                "preferred_language": language,
            },
        )

        session = self.get_session(phone_number)

        session["onboarding_completed"] = True
        session["awaiting_language"] = False
        session["current_state"] = "ready"

        return language

    # ==========================================================
    # Preferred Language
    # ==========================================================

    def get_language(
        self,
        phone_number: str,
    ) -> str:

        pref = self.preferences.get(phone_number)

        return pref.get(
            "preferred_language",
            bot_config.DEFAULT_LANGUAGE,
        )

    # ==========================================================
    # Update Activity
    # ==========================================================

    def update_activity(
        self,
        phone_number: str,
    ) -> None:

        session = self.get_session(phone_number)

        session["last_activity"] = datetime.utcnow().isoformat() + "Z"

    # ==========================================================
    # Reset Conversation
    # ==========================================================

    def reset(
        self,
        phone_number: str,
    ) -> None:

        self.sessions.pop(phone_number, None)

        self.preferences.clear(phone_number)

    # ==========================================================
    # Get Session Info
    # ==========================================================

    def session_info(
        self,
        phone_number: str,
    ) -> Dict[str, Any]:

        return deepcopy(self.get_session(phone_number))


conversation_manager = ConversationManager()
