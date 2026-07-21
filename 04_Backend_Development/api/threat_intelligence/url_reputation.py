"""
RakshakAI v2
URL Reputation Engine
"""

from __future__ import annotations

from typing import Any, Dict

from .threat_database import threat_database


class URLReputation:
    """
    URL Reputation Lookup Engine
    """

    def __init__(self) -> None:

        self.database = threat_database

    # ==========================================================
    # URL Reputation Lookup
    # ==========================================================

    def check(self, url: str) -> Dict[str, Any]:

        record = self.database.lookup_url(url)

        if record:

            return {
                "found": True,
                "indicator": url,
                "indicator_type": "url",
                "risk": record.get("risk", "unknown"),
                "category": record.get("category", "Unknown"),
                "confidence": record.get("confidence", 0),
                "source": record.get(
                    "source",
                    "RakshakAI Threat Intelligence",
                ),
                "reputation": "malicious",
                "message": "URL found in threat intelligence database.",
            }

        return {
            "found": False,
            "indicator": url,
            "indicator_type": "url",
            "risk": "safe",
            "category": None,
            "confidence": 0,
            "source": "RakshakAI Threat Intelligence",
            "reputation": "unknown",
            "message": "URL not found in threat intelligence database.",
        }


url_reputation = URLReputation()
