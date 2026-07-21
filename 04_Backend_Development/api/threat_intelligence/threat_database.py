"""
RakshakAI v2
Threat Intelligence Database

Central in-memory threat intelligence repository used by the Threat
Intelligence Platform.

This module acts as the unified lookup layer for all reputation engines.
External intelligence feeds can later replace or extend these datasets
without changing the public interface.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional


class ThreatDatabase:
    """
    Central Threat Intelligence Repository.
    """

    def __init__(self) -> None:

        self.version = "2.0"
        self.last_updated = datetime.utcnow().isoformat()

        # ---------------------------------------------------------
        # Known Malicious Domains
        # ---------------------------------------------------------

        self.domains: Dict[str, Dict[str, Any]] = {
            "paytm-security.com": {
                "risk": "critical",
                "category": "Phishing",
                "confidence": 99,
                "source": "RakshakAI Threat Intelligence",
            },
            "sbi-verify.in": {
                "risk": "critical",
                "category": "Banking Phishing",
                "confidence": 98,
                "source": "RakshakAI Threat Intelligence",
            },
            "secure-otp-login.com": {
                "risk": "high",
                "category": "Credential Theft",
                "confidence": 94,
                "source": "RakshakAI Threat Intelligence",
            },
        }

        # ---------------------------------------------------------
        # Known Malicious URLs
        # ---------------------------------------------------------

        self.urls: Dict[str, Dict[str, Any]] = {
            "http://paytm-security.com/login": {
                "risk": "critical",
                "category": "Credential Harvesting",
                "confidence": 99,
            },
            "https://sbi-verify.in/kyc": {
                "risk": "critical",
                "category": "Bank Phishing",
                "confidence": 98,
            },
        }

        # ---------------------------------------------------------
        # Malicious Email Addresses
        # ---------------------------------------------------------

        self.emails: Dict[str, Dict[str, Any]] = {
            "support@paytm-security.com": {
                "risk": "critical",
                "category": "Spoofed Sender",
                "confidence": 99,
            },
            "kyc@sbi-verify.in": {
                "risk": "critical",
                "category": "Bank Impersonation",
                "confidence": 98,
            },
        }

        # ---------------------------------------------------------
        # Fraudulent UPI IDs
        # ---------------------------------------------------------

        self.upi_ids: Dict[str, Dict[str, Any]] = {
            "verify@sbi": {
                "risk": "critical",
                "category": "UPI Fraud",
                "confidence": 97,
            },
            "refund@paytmsecure": {
                "risk": "critical",
                "category": "Refund Scam",
                "confidence": 96,
            },
        }

        # ---------------------------------------------------------
        # Malicious IP Addresses
        # ---------------------------------------------------------

        self.ip_addresses: Dict[str, Dict[str, Any]] = {
            "185.220.101.1": {
                "risk": "high",
                "category": "Known Threat Host",
                "confidence": 95,
            },
            "103.21.58.90": {
                "risk": "medium",
                "category": "Suspicious Infrastructure",
                "confidence": 81,
            },
        }

        # ---------------------------------------------------------
        # Threat Campaigns
        # ---------------------------------------------------------

        self.campaigns: Dict[str, Dict[str, Any]] = {
            "bank_kyc_campaign": {
                "name": "Bank KYC Scam",
                "severity": "critical",
                "description": "Fraud campaign targeting banking users through fake KYC updates.",
            },
            "upi_refund_campaign": {
                "name": "UPI Refund Scam",
                "severity": "high",
                "description": "Fake refund messages requesting payment authorization.",
            },
        }

    # =====================================================================
    # Generic Lookup
    # =====================================================================

    @staticmethod
    def _lookup(table: Dict[str, Dict[str, Any]], key: str) -> Optional[Dict]:

        if not key:
            return None

        key = key.strip().lower()

        result = table.get(key)

        if result is None:
            return None

        return deepcopy(result)

    # =====================================================================
    # Domain
    # =====================================================================

    def lookup_domain(self, domain: str) -> Optional[Dict]:

        return self._lookup(self.domains, domain)

    # =====================================================================
    # URL
    # =====================================================================

    def lookup_url(self, url: str) -> Optional[Dict]:

        return self._lookup(self.urls, url)

    # =====================================================================
    # Email
    # =====================================================================

    def lookup_email(self, email: str) -> Optional[Dict]:

        return self._lookup(self.emails, email)

    # =====================================================================
    # UPI
    # =====================================================================

    def lookup_upi(self, upi_id: str) -> Optional[Dict]:

        return self._lookup(self.upi_ids, upi_id)

    # =====================================================================
    # IP
    # =====================================================================

    def lookup_ip(self, ip_address: str) -> Optional[Dict]:

        return self._lookup(self.ip_addresses, ip_address)

    # =====================================================================
    # Campaign
    # =====================================================================

    def lookup_campaign(self, campaign_name: str) -> Optional[Dict]:

        return self._lookup(self.campaigns, campaign_name)

    # =====================================================================
    # Statistics
    # =====================================================================

    def statistics(self) -> Dict[str, Any]:

        return {
            "version": self.version,
            "last_updated": self.last_updated,
            "domains": len(self.domains),
            "urls": len(self.urls),
            "emails": len(self.emails),
            "upi_ids": len(self.upi_ids),
            "ip_addresses": len(self.ip_addresses),
            "campaigns": len(self.campaigns),
            "total_iocs": (
                len(self.domains)
                + len(self.urls)
                + len(self.emails)
                + len(self.upi_ids)
                + len(self.ip_addresses)
            ),
        }

    # =====================================================================
    # Export
    # =====================================================================

    def export(self) -> Dict[str, Any]:

        return {
            "metadata": {
                "version": self.version,
                "last_updated": self.last_updated,
            },
            "domains": deepcopy(self.domains),
            "urls": deepcopy(self.urls),
            "emails": deepcopy(self.emails),
            "upi_ids": deepcopy(self.upi_ids),
            "ip_addresses": deepcopy(self.ip_addresses),
            "campaigns": deepcopy(self.campaigns),
        }

    # =====================================================================
    # Search
    # =====================================================================

    def search(self, value: str) -> List[Dict[str, Any]]:

        if not value:
            return []

        value = value.lower()

        results = []

        collections = {
            "domain": self.domains,
            "url": self.urls,
            "email": self.emails,
            "upi": self.upi_ids,
            "ip": self.ip_addresses,
        }

        for indicator_type, table in collections.items():

            for indicator, details in table.items():

                if value in indicator.lower():

                    item = deepcopy(details)
                    item["indicator"] = indicator
                    item["type"] = indicator_type

                    results.append(item)

        return results


threat_database = ThreatDatabase()
