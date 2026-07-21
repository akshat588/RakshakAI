"""
RakshakAI v2
WhatsApp Message Parser

Parses incoming WhatsApp webhook payloads into a normalized format
for the Universal Investigation Engine.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


class MessageParser:
    """
    Parses WhatsApp Cloud API webhook messages.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Parse Incoming Payload
    # ==========================================================

    def parse(
        self,
        payload: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:

        try:

            entry = payload["entry"][0]
            change = entry["changes"][0]
            value = change["value"]

            message = value["messages"][0]

            sender = message.get("from")

            parsed = {
                "sender": sender,
                "message_id": message.get("id"),
                "timestamp": message.get("timestamp"),
                "message_type": message.get("type"),
                "text": None,
                "caption": None,
                "media_id": None,
                "mime_type": None,
                "filename": None,
                "raw": payload,
            }

            message_type = parsed["message_type"]

            # --------------------------------------------------
            # Text
            # --------------------------------------------------

            if message_type == "text":

                parsed["text"] = message.get("text", {}).get("body", "").strip()

            # --------------------------------------------------
            # Image
            # --------------------------------------------------

            elif message_type == "image":

                image = message.get("image", {})

                parsed["media_id"] = image.get("id")
                parsed["caption"] = image.get("caption")

            # --------------------------------------------------
            # Document
            # --------------------------------------------------

            elif message_type == "document":

                document = message.get("document", {})

                parsed["media_id"] = document.get("id")
                parsed["filename"] = document.get("filename")
                parsed["mime_type"] = document.get("mime_type")
                parsed["caption"] = document.get("caption")

            # --------------------------------------------------
            # Audio
            # --------------------------------------------------

            elif message_type == "audio":

                audio = message.get("audio", {})

                parsed["media_id"] = audio.get("id")
                parsed["mime_type"] = audio.get("mime_type")

            # --------------------------------------------------
            # Video
            # --------------------------------------------------

            elif message_type == "video":

                video = message.get("video", {})

                parsed["media_id"] = video.get("id")
                parsed["caption"] = video.get("caption")
                parsed["mime_type"] = video.get("mime_type")

            return parsed

        except Exception:

            return None


message_parser = MessageParser()
