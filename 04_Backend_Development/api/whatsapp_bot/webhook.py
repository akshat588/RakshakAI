"""
RakshakAI v2
WhatsApp Webhook

Receives webhook requests from the Meta WhatsApp Cloud API
and forwards them to the Bot Service.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from .bot_config import bot_config
from .bot_service import bot_service
from .meta_client import meta_client

whatsapp_webhook = Blueprint(
    "whatsapp_webhook",
    __name__,
)


# ==========================================================
# Webhook Verification (GET)
# ==========================================================


@whatsapp_webhook.route(
    "/webhook",
    methods=["GET"],
)
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == bot_config.VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


# ==========================================================
# Incoming Messages (POST)
# ==========================================================


@whatsapp_webhook.route(
    "/webhook",
    methods=["POST"],
)
def receive():

    payload = request.get_json(silent=True)

    if payload is None:

        return (
            jsonify(
                {
                    "success": False,
                    "message": "Invalid JSON payload.",
                }
            ),
            400,
        )

    result = bot_service.process(payload)

    try:

        if result.get("success") and "reply" in result:

            sender = None

            entries = payload.get("entry", [])

            if entries:

                changes = entries[0].get("changes", [])

                if changes:

                    value = changes[0].get("value", {})

                    messages = value.get("messages", [])

                    if messages:

                        sender = messages[0].get("from")

            if sender:

                print(f"Sender extracted: {sender}")
                print(f"Reply: {result['reply']}")
                meta_client.send_text(
                    recipient=sender,
                    message=result["reply"],
                )

    except Exception as e:

        print(f"[WhatsApp Reply Error] {e}")

    return (
        jsonify(result),
        200,
    )
