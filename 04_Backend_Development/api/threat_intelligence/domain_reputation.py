"""
RakshakAI v2
Domain Reputation Engine
"""

from __future__ import annotations

from typing import Any, Dict

from .threat_database import threat_database


class DomainReputation:
    """
    Domain Reputation Lookup Engine
    """

    def __init__(self) -> None:

        self.database = threat_database

    # ==========================================================
    # Domain Reputation Lookup
    # ==========================================================

    def check(self, domain: str) -> Dict[str, Any]:

        record = self.database.lookup_domain(domain)

        if record:

            return {
                "found": True,
                "indicator": domain,
                "indicator_type": "domain",
                "risk": record.get("risk", "unknown"),
                "category": record.get("category", "Unknown"),
                "confidence": record.get("confidence", 0),
                "source": record.get(
                    "source",
                    "RakshakAI Threat Intelligence",
                ),
                "reputation": "malicious",
                "message": "Domain found in threat intelligence database.",
            }

        return {
            "found": False,
            "indicator": domain,
            "indicator_type": "domain",
            "risk": "safe",
            "category": None,
            "confidence": 0,
            "source": "RakshakAI Threat Intelligence",
            "reputation": "unknown",
            "message": "Domain not found in threat intelligence database.",
        }


domain_reputation = DomainReputation()
