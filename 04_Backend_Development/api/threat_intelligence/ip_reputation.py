"""
RakshakAI v2
IP Reputation Engine
"""

from __future__ import annotations

from typing import Any, Dict

from .threat_database import threat_database


class IPReputation:
    """
    IP Reputation Lookup Engine
    """

    def __init__(self) -> None:

        self.database = threat_database

    # ==========================================================
    # IP Reputation Lookup
    # ==========================================================

    def check(self, ip_address: str) -> Dict[str, Any]:

        record = self.database.lookup_ip(ip_address)

        if record:

            return {
                "found": True,
                "indicator": ip_address,
                "indicator_type": "ip",
                "risk": record.get("risk", "unknown"),
                "category": record.get("category", "Unknown"),
                "confidence": record.get("confidence", 0),
                "source": record.get(
                    "source",
                    "RakshakAI Threat Intelligence",
                ),
                "reputation": "malicious",
                "message": "IP address found in threat intelligence database.",
            }

        return {
            "found": False,
            "indicator": ip_address,
            "indicator_type": "ip",
            "risk": "safe",
            "category": None,
            "confidence": 0,
            "source": "RakshakAI Threat Intelligence",
            "reputation": "unknown",
            "message": "IP address not found in threat intelligence database.",
        }


ip_reputation = IPReputation()
