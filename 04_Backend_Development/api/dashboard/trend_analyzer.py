"""
RakshakAI v2
Trend Analyzer

Generates trend information for dashboard visualizations.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


class TrendAnalyzer:
    """
    Builds daily investigation trends.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Parse Date
    # ==========================================================

    @staticmethod
    def _extract_day(timestamp: str) -> str:

        if not timestamp:
            return "Unknown"

        try:
            return datetime.fromisoformat(timestamp.replace("Z", "")).strftime("%Y-%m-%d")
        except Exception:
            return "Unknown"

    # ==========================================================
    # Daily Trend
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        daily_counter = Counter()
        severity_counter = Counter()

        for investigation in investigations:

            day = self._extract_day(investigation.get("created_at", ""))

            daily_counter[day] += 1

            severity_counter[
                investigation.get(
                    "severity",
                    "safe",
                )
            ] += 1

        return {
            "daily_activity": dict(sorted(daily_counter.items())),
            "severity_trend": dict(severity_counter),
        }


trend_analyzer = TrendAnalyzer()
