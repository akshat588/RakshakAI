"""
RakshakAI v2
Risk Distribution Engine

Generates risk score distributions for the Threat Intelligence Dashboard.
"""

from __future__ import annotations

from typing import Any, Dict, List


class RiskDistribution:
    """
    Creates risk score distribution buckets.
    """

    def __init__(self) -> None:
        self.buckets = {
            "Safe (0-19)": 0,
            "Low (20-44)": 0,
            "Medium (45-69)": 0,
            "High (70-89)": 0,
            "Critical (90-100)": 0,
        }

    # ==========================================================
    # Generate Distribution
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, int]:

        distribution = self.buckets.copy()

        for investigation in investigations:

            score = float(
                investigation.get(
                    "risk_score",
                    0,
                )
            )

            if score >= 90:
                distribution["Critical (90-100)"] += 1
            elif score >= 70:
                distribution["High (70-89)"] += 1
            elif score >= 45:
                distribution["Medium (45-69)"] += 1
            elif score >= 20:
                distribution["Low (20-44)"] += 1
            else:
                distribution["Safe (0-19)"] += 1

        return distribution


risk_distribution = RiskDistribution()
