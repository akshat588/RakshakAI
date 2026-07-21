"""
RakshakAI v2
WhatsApp Bot Configuration
"""

from __future__ import annotations

import os


class BotConfig:
    """
    Central configuration for the WhatsApp Bot.
    """

    # ==========================================================
    # Meta WhatsApp Cloud API
    # ==========================================================

    VERIFY_TOKEN = os.getenv(
        "WHATSAPP_VERIFY_TOKEN",
        "rakshakai_verify_token",
    )

    ACCESS_TOKEN = os.getenv(
        "WHATSAPP_ACCESS_TOKEN",
        "",
    )

    PHONE_NUMBER_ID = os.getenv(
        "WHATSAPP_PHONE_NUMBER_ID",
        "",
    )

    API_VERSION = os.getenv(
        "WHATSAPP_API_VERSION",
        "v23.0",
    )

    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

    # ==========================================================
    # Conversation
    # ==========================================================

    DEFAULT_LANGUAGE = "English"

    SUPPORTED_LANGUAGES = {
        "1": "English",
        "2": "Hindi",
        "3": "Punjabi",
        "4": "Marathi",
        "5": "Gujarati",
        "6": "Bengali",
        "7": "Tamil",
        "8": "Telugu",
        "9": "Kannada",
        "10": "Malayalam",
    }

    LANGUAGE_ALIASES = {
        "english": "English",
        "hindi": "Hindi",
        "हिन्दी": "Hindi",
        "punjabi": "Punjabi",
        "marathi": "Marathi",
        "gujarati": "Gujarati",
        "bengali": "Bengali",
        "bangla": "Bengali",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "kannada": "Kannada",
        "malayalam": "Malayalam",
    }

    # ==========================================================
    # Commands
    # ==========================================================

    COMMANDS = {
        "/help",
        "/language",
        "/report",
        "/technical",
        "/summary",
        "/start",
    }

    # ==========================================================
    # User Messages
    # ==========================================================

    WELCOME_MESSAGE = (
        "👋 Welcome to RakshakAI!\n\n"
        "Before we begin, please choose your preferred language.\n\n"
        "1️⃣ English\n"
        "2️⃣ हिन्दी (Hindi)\n"
        "3️⃣ ਪੰਜਾਬੀ (Punjabi)\n"
        "4️⃣ मराठी (Marathi)\n"
        "5️⃣ ગુજરાતી (Gujarati)\n"
        "6️⃣ বাংলা (Bengali)\n"
        "7️⃣ தமிழ் (Tamil)\n"
        "8️⃣ తెలుగు (Telugu)\n"
        "9️⃣ ಕನ್ನಡ (Kannada)\n"
        "🔟 മലയാളം (Malayalam)\n\n"
        "Reply with the number or language name."
    )

    HELP_MESSAGE = (
        "You can send:\n\n"
        "• Suspicious Links\n"
        "• Emails\n"
        "• SMS\n"
        "• WhatsApp Messages\n"
        "• QR Codes\n"
        "• Screenshots\n"
        "• PDFs\n"
        "• Images\n\n"
        "I'll investigate them and explain the result in simple language."
    )

    SIMPLE_MODE = True


bot_config = BotConfig()
