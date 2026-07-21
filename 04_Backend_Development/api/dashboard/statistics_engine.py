"""
RakshakAI v2
Statistics Engine

Provides aggregated statistics for the Threat Intelligence Dashboard.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


class StatisticsEngine:
    """
    Aggregates investigation statistics.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Investigation Statistics
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        severity_counter = Counter()
        type_counter = Counter()

        malicious = 0
        safe = 0

        total_score = 0.0

        for investigation in investigations:

            severity = investigation.get(
                "severity",
                "safe",
            )

            detected_type = investigation.get(
                "detected_type",
                "unknown",
            )

            prediction = str(
                investigation.get(
                    "prediction",
                    "",
                )
            ).lower()

            severity_counter[severity] += 1
            type_counter[detected_type] += 1

            total_score += float(
                investigation.get(
                    "risk_score",
                    0,
                )
            )

            if prediction in {
                "malicious",
                "scam",
                "phishing",
                "fraud",
            }:
                malicious += 1
            else:
                safe += 1

        total = len(investigations)

        average_score = round(total_score / total, 2) if total else 0

        return {
            "total_investigations": total,
            "malicious": malicious,
            "safe": safe,
            "average_risk_score": average_score,
            "severity_distribution": dict(severity_counter),
            "type_distribution": dict(type_counter),
        }

    # ==========================================================
    # Empty Dashboard
    # ==========================================================

    def empty(self) -> Dict[str, Any]:

        return {
            "total_investigations": 0,
            "malicious": 0,
            "safe": 0,
            "average_risk_score": 0,
            "severity_distribution": {},
            "type_distribution": {},
        }


statistics_engine = StatisticsEngine()
