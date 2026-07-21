"""
RakshakAI v2
WhatsApp Bot Service

Coordinates the complete WhatsApp bot workflow.
"""

from __future__ import annotations

from typing import Any, Dict

from .conversation_manager import conversation_manager
from .command_handler import command_handler
from .message_parser import message_parser
from .media_handler import media_handler
from .response_builder import response_builder
from api.assistant_core.detector import UniversalInputDetector
from api.assistant_core.router import UniversalRouter
from api.assistant_core.investigation import InvestigationEngine


class BotService:
    """
    Main WhatsApp Bot Service.
    """

    def __init__(self) -> None:

        self.conversations = conversation_manager
        self.commands = command_handler
        self.parser = message_parser
        self.media = media_handler
        self.responses = response_builder
        self.router = UniversalRouter
        self.investigation = InvestigationEngine

    # ==========================================================
    # Handle Incoming Message
    # ==========================================================

    def process(
        self,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        parsed = self.parser.parse(payload)

        if parsed is None:

            return {
                "success": False,
                "reply": "Unable to process this message.",
            }

        phone = parsed["sender"]

        self.conversations.update_activity(phone)

        # ------------------------------------------------------
        # First-time onboarding
        # ------------------------------------------------------

        if self.conversations.requires_onboarding(phone):

            if parsed["message_type"] == "text":

                language = self.conversations.save_language(
                    phone,
                    parsed["text"],
                )

                if language:

                    return {
                        "success": True,
                        "reply": self.responses.language_selected(language),
                    }

            return {
                "success": True,
                "reply": (
                    "👋 Welcome to RakshakAI!\n\n"
                    "Please choose your preferred language "
                    "by replying with a number or language name."
                ),
            }

        # ------------------------------------------------------
        # Commands
        # ------------------------------------------------------

        if parsed["message_type"] == "text" and self.commands.is_command(parsed["text"]):

            result = self.commands.execute(
                phone,
                parsed["text"],
            )

            return {
                "success": True,
                "reply": result["reply"],
            }

        # ------------------------------------------------------
        # Media
        # ------------------------------------------------------

        if self.media.is_supported(parsed["message_type"]):

            media = self.media.prepare(parsed)

            return {
                "success": True,
                "action": "investigate_media",
                "media": media,
            }

        # ------------------------------------------------------
        # Text Investigation
        # ------------------------------------------------------

        content = parsed.get("text", "")

        try:
            input_type = UniversalInputDetector.detect(content)

            engine_result = UniversalRouter.analyze(
                input_type=input_type,
                content=content,
            )

            report = InvestigationEngine.build(
                analyzer=input_type,
                engine_result=engine_result,
                original_input=content,
            )

            return {
                "success": True,
                "action": "reply",
                "report": report,
                "sender": phone,
            }

        except Exception as e:

            return {
                "success": False,
                "reply": f"❌ Investigation failed: {str(e)}",
            }


bot_service = BotService()
