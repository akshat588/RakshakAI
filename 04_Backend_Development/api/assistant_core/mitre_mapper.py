"""
==========================================================
RakshakAI v2
MITRE ATT&CK Mapper
==========================================================
"""

from __future__ import annotations

from typing import Dict


class MITREMapper:

    def __init__(self):

        self.techniques = {
            "url": {
                "id": "T1566.002",
                "name": "Phishing: Spearphishing Link",
                "tactic": "Initial Access",
            },
            "email": {
                "id": "T1566.001",
                "name": "Phishing: Spearphishing Attachment",
                "tactic": "Initial Access",
            },
            "sms": {
                "id": "T1660",
                "name": "Phishing via SMS",
                "tactic": "Initial Access",
            },
            "whatsapp": {
                "id": "T1660",
                "name": "Phishing via Messaging Service",
                "tactic": "Initial Access",
            },
            "upi": {
                "id": "T1656",
                "name": "Financial Transaction Fraud",
                "tactic": "Credential Access",
            },
            "fake_job": {
                "id": "T1585",
                "name": "Establish Accounts",
                "tactic": "Resource Development",
            },
            "social_engineering": {
                "id": "T1204",
                "name": "User Execution",
                "tactic": "Execution",
            },
            "qr": {
                "id": "T1204",
                "name": "User Execution",
                "tactic": "Execution",
            },
            "deepfake": {
                "id": "T1585",
                "name": "Identity Manipulation",
                "tactic": "Defense Evasion",
            },
            "voice": {
                "id": "T1598",
                "name": "Phishing for Information",
                "tactic": "Reconnaissance",
            },
        }

    def map(self, report: Dict) -> Dict:

        mappings = []

        for engine in report.get("executed_engines", []):

            if engine in self.techniques:

                mappings.append({"engine": engine, **self.techniques[engine]})

        return {"count": len(mappings), "techniques": mappings}
