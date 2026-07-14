"""
==========================================================
RakshakAI v2
Recommendation Engine
==========================================================
"""

from __future__ import annotations

from typing import Dict


class RecommendationEngine:

    def generate(self, report: Dict) -> Dict:

        actions = []

        risk = report.get("overall_risk", "UNKNOWN")

        engines = report.get("executed_engines", [])

        if risk == "CRITICAL":

            actions.extend(
                [
                    "Immediately stop interacting with the content.",
                    "Block the sender or source.",
                    "Report the incident to the relevant platform.",
                    "Run a complete device security scan.",
                    "Change passwords for affected accounts.",
                ]
            )

        elif risk == "HIGH":

            actions.extend(
                [
                    "Avoid clicking any links or attachments.",
                    "Verify the sender independently.",
                    "Monitor financial accounts for suspicious activity.",
                ]
            )

        elif risk == "MEDIUM":

            actions.extend(
                [
                    "Manually verify the authenticity before proceeding.",
                    "Do not share personal or financial information.",
                ]
            )

        else:

            actions.append("No immediate action is required.")

        if "upi" in engines:

            actions.extend(
                ["Do not approve unknown UPI collect requests.", "Never share your UPI PIN."]
            )

        if "email" in engines:

            actions.append("Inspect the sender domain carefully.")

        if "url" in engines:

            actions.append("Open suspicious URLs only inside an isolated sandbox.")

        if "sms" in engines or "whatsapp" in engines:

            actions.append("Do not reply to suspicious messages.")

        return {"count": len(set(actions)), "actions": list(dict.fromkeys(actions))}
