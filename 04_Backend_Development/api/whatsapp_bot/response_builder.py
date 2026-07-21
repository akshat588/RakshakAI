"""
RakshakAI v2
WhatsApp Response Builder

Builds user-friendly WhatsApp responses in simple language.
"""

from __future__ import annotations

from typing import Any, Dict


class ResponseBuilder:
    """
    Creates simple responses for end users.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Welcome
    # ==========================================================

    @staticmethod
    def language_selected(language: str) -> str:

        return (
            f"✅ Language set to {language}.\n\n"
            "You can now send:\n"
            "• Links\n"
            "• Emails\n"
            "• SMS\n"
            "• WhatsApp messages\n"
            "• QR Codes\n"
            "• Screenshots\n"
            "• Images\n"
            "• PDF files\n\n"
            "I'll explain whether they are safe or suspicious in simple language."
        )

    # ==========================================================
    # Investigation Result
    # ==========================================================

    def build_simple_response(
        self,
        investigation: Dict[str, Any],
    ) -> str:

        prediction = investigation.get(
            "prediction",
            "Unknown",
        )

        severity = investigation.get(
            "severity",
            "safe",
        ).upper()

        confidence = investigation.get(
            "confidence",
            0,
        )

        summary = investigation.get(
            "executive_summary",
            "Analysis completed.",
        )

        recommendations = investigation.get(
            "recommendations",
            [],
        )

        response = (
            f"🛡️ RakshakAI Investigation Result\n\n"
            f"Threat Level: {severity}\n"
            f"Prediction: {prediction}\n"
            f"Confidence: {confidence}%\n\n"
            f"{summary}\n"
        )

        if recommendations:

            response += "\nWhat you should do:\n"

            for recommendation in recommendations[:5]:
                response += f"• {recommendation}\n"

        return response.strip()

    # ==========================================================
    # Technical Report
    # ==========================================================

    def build_technical_response(
        self,
        investigation: Dict[str, Any],
    ) -> str:

        return (
            f"Risk Score: {investigation.get('risk_score', 0)}\n"
            f"Severity: {investigation.get('severity', 'safe')}\n"
            f"MITRE Techniques: "
            f"{len(investigation.get('mitre_attack', []))}\n"
            f"Indicators of Compromise: "
            f"{len(investigation.get('iocs', []))}"
        )


response_builder = ResponseBuilder()
