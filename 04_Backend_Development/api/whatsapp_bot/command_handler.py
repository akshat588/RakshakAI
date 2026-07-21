"""
RakshakAI v2
WhatsApp Command Handler

Handles user commands before normal investigation starts.
"""

from __future__ import annotations

from typing import Any, Dict

from .bot_config import bot_config
from .conversation_manager import conversation_manager


class CommandHandler:
    """
    Handles supported WhatsApp commands.
    """

    def __init__(self) -> None:

        self.config = bot_config
        self.conversations = conversation_manager

    # ==========================================================
    # Command Detection
    # ==========================================================

    def is_command(
        self,
        text: str | None,
    ) -> bool:

        if not text:
            return False

        return text.strip().lower() in {command.lower() for command in self.config.COMMANDS}

    # ==========================================================
    # Execute Command
    # ==========================================================

    def execute(
        self,
        phone_number: str,
        command: str,
    ) -> Dict[str, Any]:

        command = command.strip().lower()

        # -----------------------------------------------
        # Start
        # -----------------------------------------------

        if command == "/start":

            self.conversations.reset(phone_number)

            return {
                "handled": True,
                "reply": self.config.WELCOME_MESSAGE,
            }

        # -----------------------------------------------
        # Help
        # -----------------------------------------------

        if command == "/help":

            return {
                "handled": True,
                "reply": self.config.HELP_MESSAGE,
            }

        # -----------------------------------------------
        # Language
        # -----------------------------------------------

        if command == "/language":

            session = self.conversations.get_session(phone_number)

            session["awaiting_language"] = True
            session["current_state"] = "language_selection"

            return {
                "handled": True,
                "reply": self.config.WELCOME_MESSAGE,
            }

        # -----------------------------------------------
        # Report
        # -----------------------------------------------

        if command == "/report":

            return {
                "handled": True,
                "reply": (
                    "📄 Send the message, email, link, QR code, "
                    "PDF, or screenshot you want me to analyze."
                ),
            }

        # -----------------------------------------------
        # Technical Report
        # -----------------------------------------------

        if command == "/technical":

            return {
                "handled": True,
                "reply": (
                    "🛡️ Technical Mode enabled for the next "
                    "investigation. I'll include detailed "
                    "security findings after the analysis."
                ),
            }

        # -----------------------------------------------
        # Summary
        # -----------------------------------------------

        if command == "/summary":

            return {
                "handled": True,
                "reply": (
                    "📋 I'll provide a short and simple summary " "after your next investigation."
                ),
            }

        # -----------------------------------------------
        # Unknown
        # -----------------------------------------------

        return {
            "handled": False,
            "reply": None,
        }


command_handler = CommandHandler()
