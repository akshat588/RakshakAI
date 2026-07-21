"""
RakshakAI v2
Recent Investigations

Provides a normalized list of recent investigations for the dashboard.
"""

from __future__ import annotations

from typing import Any, Dict, List


class RecentInvestigations:
    """
    Builds the recent investigations panel.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Generate
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        ordered = sorted(
            investigations,
            key=lambda item: item.get("created_at", ""),
            reverse=True,
        )

        results = []

        for investigation in ordered[:limit]:

            results.append(
                {
                    "case_id": investigation.get("case_id"),
                    "title": investigation.get(
                        "title",
                        "Investigation",
                    ),
                    "detected_type": investigation.get(
                        "detected_type",
                        "unknown",
                    ),
                    "prediction": investigation.get(
                        "prediction",
                        "unknown",
                    ),
                    "severity": investigation.get(
                        "severity",
                        "safe",
                    ),
                    "risk_score": investigation.get(
                        "risk_score",
                        0,
                    ),
                    "confidence": investigation.get(
                        "confidence",
                        0,
                    ),
                    "created_at": investigation.get(
                        "created_at",
                    ),
                }
            )

        return results


recent_investigations = RecentInvestigations()
