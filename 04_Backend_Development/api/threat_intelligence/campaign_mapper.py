"""
RakshakAI v2
Threat Campaign Mapper

Maps investigation indicators to known fraud campaigns.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .threat_database import threat_database


class CampaignMapper:
    """
    Maps indicators to known scam campaigns.
    """

    def __init__(self) -> None:

        self.database = threat_database

    # ==========================================================
    # Campaign Mapping
    # ==========================================================

    def map_campaign(
        self,
        indicators: List[str],
    ) -> Dict[str, Any]:

        matched_campaigns = []

        indicator_text = " ".join(str(i).lower() for i in indicators if i)

        campaign_rules = {
            "bank_kyc_campaign": [
                "kyc",
                "verify",
                "bank",
                "otp",
                "account",
                "sbi",
                "hdfc",
                "icici",
            ],
            "upi_refund_campaign": [
                "refund",
                "cashback",
                "reward",
                "upi",
                "collect",
                "payment",
            ],
        }

        for campaign_key, keywords in campaign_rules.items():

            if any(keyword in indicator_text for keyword in keywords):

                campaign = self.database.lookup_campaign(campaign_key)

                if campaign:

                    matched_campaigns.append(campaign)

        severity = "safe"

        if matched_campaigns:

            priorities = {
                "safe": 0,
                "low": 1,
                "medium": 2,
                "high": 3,
                "critical": 4,
            }

            severity = max(
                (campaign.get("severity", "safe") for campaign in matched_campaigns),
                key=lambda value: priorities.get(value, 0),
            )

        return {
            "campaign_detected": len(matched_campaigns) > 0,
            "campaign_count": len(matched_campaigns),
            "severity": severity,
            "campaigns": matched_campaigns,
        }

    # ==========================================================
    # Batch Mapping
    # ==========================================================

    def batch_map(
        self,
        investigations: List[List[str]],
    ) -> List[Dict[str, Any]]:

        return [self.map_campaign(indicators) for indicators in investigations]


campaign_mapper = CampaignMapper()
