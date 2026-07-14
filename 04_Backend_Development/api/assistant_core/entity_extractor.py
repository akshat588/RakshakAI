"""
==========================================================
RakshakAI v2
Universal Entity Extractor
==========================================================
"""

from __future__ import annotations

import re
from datetime import datetime


class UniversalEntityExtractor:

    def __init__(self):

        self.upi_pattern = re.compile(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b")

        self.amount_pattern = re.compile(
            r"(?:₹|rs\.?|inr)?\s*([0-9,]+(?:\.[0-9]{1,2})?)",
            re.IGNORECASE,
        )

        self.url_pattern = re.compile(r"https?://[^\s]+")

    def extract_upi(self, text: str):

        match = self.upi_pattern.search(text)

        return match.group(0) if match else ""

    def extract_amount(self, text: str):

        match = self.amount_pattern.search(text)

        if not match:

            return 0.0

        return float(match.group(1).replace(",", ""))

    def extract_bank(self, text: str):

        banks = ["SBI", "HDFC", "ICICI", "Axis", "PNB", "BOB", "Canara", "Kotak", "Paytm"]

        lower = text.lower()

        for bank in banks:

            if bank.lower() in lower:

                return bank

        return "Unknown Bank"

    def extract_channel(self, text: str):

        lower = text.lower()

        if "qr" in lower:

            return "QR"

        if "upi" in lower:

            return "UPI"

        return "UPI"

    def build_upi_features(self, text: str):

        amount = self.extract_amount(text)

        now = datetime.now()

        return {
            "Bank_Name": self.extract_bank(text),
            "Transaction_Amount": amount,
            "Transaction_Date": now.strftime("%Y-%m-%d"),
            "Transaction_Time": now.strftime("%H:%M"),
            "Merchant_Name": self.extract_upi(text) or "Unknown",
            "Location_City": "Unknown",
            "Location_State": "Unknown",
            "Transaction_Type": "Debit",
            "Channel": self.extract_channel(text),
        }


extractor = UniversalEntityExtractor()
