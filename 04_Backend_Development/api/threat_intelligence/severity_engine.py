"""
RakshakAI v2
Threat Severity Engine

Calculates the final threat severity using reputation, analyzer
confidence, IOC correlation, MITRE mapping and investigation results.
"""

from __future__ import annotations

from typing import Any, Dict, List


class SeverityEngine:

    def __init__(self) -> None:

        self.levels = {
            "safe": 0,
            "low": 20,
            "medium": 45,
            "high": 70,
            "critical": 90,
        }

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    @staticmethod
    def _normalize(value: float) -> float:

        return max(0.0, min(100.0, value))

    # ==========================================================
    # Risk Score
    # ==========================================================

    def calculate_score(
        self,
        analyzer_confidence: float = 0,
        reputation_confidence: float = 0,
        ioc_count: int = 0,
        mitre_count: int = 0,
        malicious_analyzers: int = 0,
    ) -> float:

        score = 0

        score += analyzer_confidence * 0.45
        score += reputation_confidence * 0.30
        score += min(ioc_count * 4, 12)
        score += min(mitre_count * 2, 8)
        score += min(malicious_analyzers * 5, 15)

        return round(self._normalize(score), 2)

    # ==========================================================
    # Severity
    # ==========================================================

    def get_severity(self, score: float) -> str:

        if score >= 90:
            return "critical"

        if score >= 70:
            return "high"

        if score >= 45:
            return "medium"

        if score >= 20:
            return "low"

        return "safe"

    # ==========================================================
    # Public Engine
    # ==========================================================

    def evaluate(
        self,
        analyzer_confidence: float = 0,
        reputation_confidence: float = 0,
        ioc_count: int = 0,
        mitre_count: int = 0,
        malicious_analyzers: int = 0,
    ) -> Dict[str, Any]:

        score = self.calculate_score(
            analyzer_confidence=analyzer_confidence,
            reputation_confidence=reputation_confidence,
            ioc_count=ioc_count,
            mitre_count=mitre_count,
            malicious_analyzers=malicious_analyzers,
        )

        return {
            "risk_score": score,
            "severity": self.get_severity(score),
        }

    # ==========================================================
    # Batch Evaluation
    # ==========================================================

    def batch_evaluate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        results = []

        for item in investigations:

            result = self.evaluate(
                analyzer_confidence=item.get("confidence", 0),
                reputation_confidence=item.get(
                    "reputation_confidence",
                    0,
                ),
                ioc_count=item.get("ioc_count", 0),
                mitre_count=item.get("mitre_count", 0),
                malicious_analyzers=item.get(
                    "malicious_analyzers",
                    0,
                ),
            )

            enriched = dict(item)
            enriched.update(result)

            results.append(enriched)

        return results


severity_engine = SeverityEngine()
