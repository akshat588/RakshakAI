"""
==========================================================
RakshakAI v2
Threat Explanation Engine
==========================================================
"""

from __future__ import annotations

from typing import Dict


class ThreatExplainer:

    def explain(self, report: Dict) -> Dict:

        risk = report.get("overall_risk", "UNKNOWN")

        engines = report.get("executed_engines", [])

        evidence = report.get("evidence", [])

        explanation = []

        if risk == "CRITICAL":

            explanation.append("Multiple high-confidence cyber threat indicators were detected.")

        elif risk == "HIGH":

            explanation.append("Several suspicious indicators suggest a likely cyber attack.")

        elif risk == "MEDIUM":

            explanation.append("Potential malicious activity requires manual verification.")

        elif risk == "LOW":

            explanation.append("Only minor suspicious indicators were detected.")

        else:

            explanation.append("No significant malicious indicators were detected.")

        if "email" in engines:

            explanation.append("Email characteristics match known phishing behaviour.")

        if "url" in engines:

            explanation.append("Embedded URLs exhibit phishing characteristics.")

        if "upi" in engines:

            explanation.append("Financial payment indicators were identified.")

        if "sms" in engines:

            explanation.append("SMS content contains fraud-related indicators.")

        if "whatsapp" in engines:

            explanation.append("Messaging content matches common scam patterns.")

        if "social_engineering" in engines:

            explanation.append("Psychological manipulation techniques were detected.")

        if len(evidence) > 0:

            explanation.append(f"{len(evidence)} evidence item(s) support the investigation.")

        return {"summary": " ".join(explanation), "evidence_count": len(evidence), "risk": risk}
