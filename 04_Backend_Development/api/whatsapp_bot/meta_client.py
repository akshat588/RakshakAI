"""
RakshakAI v2
Meta WhatsApp Cloud API Client

Responsible only for sending messages to the
WhatsApp Cloud API.
"""

from __future__ import annotations

import requests

from .bot_config import bot_config


class MetaClient:
    """
    Meta WhatsApp Cloud API Client.
    """

    def __init__(self) -> None:

        self.base_url = f"{bot_config.BASE_URL}/" f"{bot_config.PHONE_NUMBER_ID}/messages"

        self.headers = {
            "Authorization": f"Bearer {bot_config.ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    # ==========================================================
    # Send Text Message
    # ==========================================================

    def send_text(
        self,
        recipient: str,
        message: str,
    ):

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {
                "body": message,
            },
        }

        print("\n========== OUTGOING ==========")
        print("Recipient:", recipient)
        print("Payload:", payload)
        print("==============================")

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=30,
        )

        print("Access Token:", bot_config.ACCESS_TOKEN[:20] + "...")
        print("Phone Number ID:", bot_config.PHONE_NUMBER_ID)

        response.raise_for_status()

        return response.json()

    # Singleton instance


meta_client = MetaClient()
