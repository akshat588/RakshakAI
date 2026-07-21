"""
RakshakAI v2
WhatsApp Media Handler

Handles media received from the WhatsApp Cloud API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional


class MediaHandler:
    """
    Handles image, document, audio and video metadata.

    NOTE:
    Actual media download from the WhatsApp Cloud API will be
    connected during production configuration.
    """

    def __init__(self) -> None:

        self.supported_types = {
            "image",
            "document",
            "audio",
            "video",
        }

    # ==========================================================
    # Supported Media
    # ==========================================================

    def is_supported(
        self,
        message_type: str,
    ) -> bool:

        return message_type.lower() in self.supported_types

    # ==========================================================
    # Build Media Information
    # ==========================================================

    def prepare(
        self,
        parsed_message: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "message_type": parsed_message.get("message_type"),
            "media_id": parsed_message.get("media_id"),
            "filename": parsed_message.get("filename"),
            "mime_type": parsed_message.get("mime_type"),
            "caption": parsed_message.get("caption"),
            "status": "pending_download",
        }

    # ==========================================================
    # Download Placeholder
    # ==========================================================

    def download(
        self,
        media_info: Dict[str, Any],
    ) -> Optional[Path]:
        """
        Placeholder for WhatsApp Cloud API media download.

        Production implementation will:
        1. Request media URL
        2. Download file
        3. Save locally
        4. Return local path
        """

        return None


media_handler = MediaHandler()
