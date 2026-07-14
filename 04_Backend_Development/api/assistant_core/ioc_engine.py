"""
==========================================================
RakshakAI v2
IOC Correlation Engine
==========================================================
"""

from __future__ import annotations

from typing import Dict
from typing import List
import re


class IOCEngine:

    def __init__(self):

        self.url_pattern = re.compile(r"https?://[^\s]+")

        self.email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

        self.upi_pattern = re.compile(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b")

        self.ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

        self.phone_pattern = re.compile(r"(?:\+91[- ]?)?[6-9]\d{9}")

    def analyze(self, report: Dict) -> Dict:

        iocs = []

        text = self.collect_text(report)

        iocs.extend(self.find_urls(text))

        iocs.extend(self.find_emails(text))

        iocs.extend(self.find_upi(text))

        iocs.extend(self.find_ips(text))

        iocs.extend(self.find_phones(text))

        return {"count": len(iocs), "items": list(dict.fromkeys(iocs))}

    def collect_text(self, report: Dict) -> str:

        chunks: List[str] = []

        chunks.extend(report.get("evidence", []))

        chunks.extend(report.get("iocs", []))

        for result in report.get("results", []):

            chunks.extend(result.get("evidence", []))

            chunks.extend(result.get("iocs", []))

        return "\n".join(map(str, chunks))

    def find_urls(self, text):

        return self.url_pattern.findall(text)

    def find_emails(self, text):

        return self.email_pattern.findall(text)

    def find_upi(self, text):

        return self.upi_pattern.findall(text)

    def find_ips(self, text):

        return self.ip_pattern.findall(text)

    def find_phones(self, text):

        return self.phone_pattern.findall(text)
