"""
RakshakAI v2
Case Statistics

Generates statistics for stored investigation cases.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List


class CaseStatistics:
    """
    Case statistics engine.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Generate Statistics
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        severity_counter = Counter()
        type_counter = Counter()
        prediction_counter = Counter()

        total_risk_score = 0.0

        for investigation in investigations:

            severity_counter[
                investigation.get(
                    "severity",
                    "safe",
                )
            ] += 1

            type_counter[
                investigation.get(
                    "detected_type",
                    "unknown",
                )
            ] += 1

            prediction_counter[
                str(
                    investigation.get(
                        "prediction",
                        "unknown",
                    )
                ).lower()
            ] += 1

            total_risk_score += float(
                investigation.get(
                    "risk_score",
                    0,
                )
            )

        total_cases = len(investigations)

        average_risk_score = round(total_risk_score / total_cases, 2) if total_cases else 0

        return {
            "total_cases": total_cases,
            "average_risk_score": average_risk_score,
            "severity_distribution": dict(severity_counter),
            "type_distribution": dict(type_counter),
            "prediction_distribution": dict(prediction_counter),
        }


case_statistics = CaseStatistics()
