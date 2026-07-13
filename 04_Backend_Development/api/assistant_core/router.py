"""
Universal Router
RakshakAI v2

Routes detected input types to the appropriate analyzer.
"""

from __future__ import annotations

from api.assistant_core.detector import InputType


class UniversalRouter:

    ROUTES = {
        InputType.EMAIL: "email",
        InputType.URL: "url",
        InputType.SMS: "sms",
        InputType.WHATSAPP: "whatsapp",
        InputType.UPI: "upi",
        InputType.FAKE_JOB: "fake_job",
        InputType.SOCIAL_ENGINEERING: "social_engineering",
        InputType.QR: "qr",
        InputType.DEEPFAKE: "deepfake",
        InputType.VOICE: "voice",
    }

    @classmethod
    def get_route(cls, input_type: str):

        return cls.ROUTES.get(input_type)
