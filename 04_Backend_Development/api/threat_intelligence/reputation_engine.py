"""
RakshakAI v2
Threat Intelligence Reputation Engine

Central reputation engine that aggregates reputation results from all
individual reputation modules.

This acts as the single interface for the Universal Investigation
Orchestrator.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .domain_reputation import DomainReputation
from .url_reputation import URLReputation
from .email_reputation import EmailReputation
from .upi_reputation import UPIReputation
from .ip_reputation import IPReputation


class ReputationEngine:
    """
    Central Reputation Engine
    """

    def __init__(self) -> None:

        self.domain_engine = DomainReputation()
        self.url_engine = URLReputation()
        self.email_engine = EmailReputation()
        self.upi_engine = UPIReputation()
        self.ip_engine = IPReputation()

    # ============================================================
    # Domain
    # ============================================================

    def check_domain(self, domain: str) -> Dict[str, Any]:

        return self.domain_engine.check(domain)

    # ============================================================
    # URL
    # ============================================================

    def check_url(self, url: str) -> Dict[str, Any]:

        return self.url_engine.check(url)

    # ============================================================
    # Email
    # ============================================================

    def check_email(self, email: str) -> Dict[str, Any]:

        return self.email_engine.check(email)

    # ============================================================
    # UPI
    # ============================================================

    def check_upi(self, upi_id: str) -> Dict[str, Any]:

        return self.upi_engine.check(upi_id)

    # ============================================================
    # IP
    # ============================================================

    def check_ip(self, ip_address: str) -> Dict[str, Any]:

        return self.ip_engine.check(ip_address)

    # ============================================================
    # Generic Dispatcher
    # ============================================================

    def check(
        self,
        indicator: str,
        indicator_type: str,
    ) -> Dict[str, Any]:

        indicator_type = indicator_type.lower().strip()

        dispatch = {
            "domain": self.check_domain,
            "url": self.check_url,
            "email": self.check_email,
            "upi": self.check_upi,
            "ip": self.check_ip,
        }

        handler = dispatch.get(indicator_type)

        if handler is None:

            return {
                "found": False,
                "indicator": indicator,
                "indicator_type": indicator_type,
                "risk": "unknown",
                "confidence": 0,
                "message": "Unsupported indicator type.",
            }

        return handler(indicator)

    # ============================================================
    # Batch Reputation
    # ============================================================

    def batch_check(
        self,
        indicators: Dict[str, str],
    ) -> Dict[str, Dict[str, Any]]:

        results = {}

        for indicator, indicator_type in indicators.items():

            results[indicator] = self.check(
                indicator,
                indicator_type,
            )

        return results


reputation_engine = ReputationEngine()
