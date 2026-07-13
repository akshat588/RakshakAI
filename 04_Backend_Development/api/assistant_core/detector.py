"""
Universal Input Detector
RakshakAI v2
"""

from __future__ import annotations

import re


class InputType:
    URL = "url"
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    QR = "qr"
    UPI = "upi"
    FAKE_JOB = "fake_job"
    SOCIAL_ENGINEERING = "social_engineering"
    DEEPFAKE = "deepfake"
    VOICE = "voice"
    UNKNOWN = "unknown"


class UniversalInputDetector:
    URL_PATTERN = re.compile(r"(https?://[^\s]+|www\.[^\s]+)", re.IGNORECASE)

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    UPI_PATTERN = re.compile(r"^[\w.\-]{2,}@[A-Za-z]+$")

    WHATSAPP_HINTS = (
        "forwarded",
        "forwarded many times",
        "this message was deleted",
        "joined using this group's invite link",
        "whatsapp",
    )

    JOB_HINTS = (
        "salary",
        "job",
        "hiring",
        "vacancy",
        "recruitment",
        "resume",
        "work from home",
        "interview",
    )

    SOCIAL_HINTS = (
        "urgent",
        "otp",
        "verify",
        "password",
        "bank account",
        "gift card",
        "click now",
        "security team",
    )

    @classmethod
    def detect(cls, text: str) -> str:
        if not text:
            return InputType.UNKNOWN

        text = text.strip()

        if cls.EMAIL_PATTERN.fullmatch(text):
            return InputType.EMAIL

        if cls.UPI_PATTERN.fullmatch(text):
            return InputType.UPI

        if cls.URL_PATTERN.search(text):
            return InputType.URL

        lower = text.lower()

        if any(hint in lower for hint in cls.WHATSAPP_HINTS):
            return InputType.WHATSAPP

        if any(hint in lower for hint in cls.JOB_HINTS):
            return InputType.FAKE_JOB

        if any(hint in lower for hint in cls.SOCIAL_HINTS):
            return InputType.SOCIAL_ENGINEERING

        if len(text.split()) <= 30:
            return InputType.SMS

        return InputType.UNKNOWN
