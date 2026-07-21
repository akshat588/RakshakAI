"""
Universal Router
RakshakAI v2
"""

from __future__ import annotations

from api.assistant_core.detector import InputType

# Import reusable AI engines
from api.email import analyze_email_ai
from api.url import analyze_url_ai
from api.sms import analyze_sms_ai
from api.whatsapp import analyze_whatsapp_ai
from api.upi import analyze_upi_ai
from api.qr import analyze_qr_ai
from api.fake_job import analyze_fake_job_ai
from api.social_engineering import analyze_social_engineering_ai


class UniversalRouter:

    ROUTES = {
        InputType.EMAIL: analyze_email_ai,
        InputType.URL: analyze_url_ai,
        InputType.SMS: analyze_sms_ai,
    }

    @classmethod
    def analyze(cls, input_type: str, content: str):

        analyzer = cls.ROUTES.get(input_type)

        if analyzer is None:
            raise ValueError(f"No analyzer registered for '{input_type}'")

        return analyzer(content)
