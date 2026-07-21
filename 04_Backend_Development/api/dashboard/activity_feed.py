"""
RakshakAI v2
Activity Feed

Builds the recent activity feed for the Threat Intelligence Dashboard.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


class ActivityFeed:
    """
    Generates dashboard activity feed entries.
    """

    def __init__(self) -> None:
        pass

    # ==========================================================
    # Feed Item
    # ==========================================================

    @staticmethod
    def _create_feed_item(
        investigation: Dict[str, Any],
    ) -> Dict[str, Any]:

        return {
            "timestamp": investigation.get(
                "created_at",
                datetime.utcnow().isoformat() + "Z",
            ),
            "title": investigation.get(
                "title",
                "Threat Investigation",
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
        }

    # ==========================================================
    # Generate Feed
    # ==========================================================

    def generate(
        self,
        investigations: List[Dict[str, Any]],
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        ordered = sorted(
            investigations,
            key=lambda item: item.get(
                "created_at",
                "",
            ),
            reverse=True,
        )

        return [self._create_feed_item(item) for item in ordered[:limit]]


activity_feed = ActivityFeed()
