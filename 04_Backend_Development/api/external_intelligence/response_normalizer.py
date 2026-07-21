"""
RakshakAI v2
External Intelligence Response Normalizer

Normalizes responses from different external threat intelligence
providers into a unified schema.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict


class ResponseNormalizer:
    """
    Converts provider-specific responses into the RakshakAI
    standard response format.
    """

    def __init__(self) -> None:

        self.default_response = {
            "provider": None,
            "indicator": None,
            "indicator_type": None,
            "found": False,
            "risk": "unknown",
            "confidence": 0,
            "category": None,
            "source": "External Threat Intelligence",
            "timestamp": None,
            "details": {},
        }

    # ==========================================================
    # Normalize
    # ==========================================================

    def normalize(
        self,
        provider: str,
        indicator: str,
        indicator_type: str,
        response: Dict[str, Any] | None,
    ) -> Dict[str, Any]:

        result = deepcopy(self.default_response)

        result["provider"] = provider
        result["indicator"] = indicator
        result["indicator_type"] = indicator_type
        result["timestamp"] = datetime.utcnow().isoformat() + "Z"

        if not response:
            return result

        result.update(response)

        result["provider"] = provider
        result["indicator"] = indicator
        result["indicator_type"] = indicator_type

        return result

    # ==========================================================
    # Error Response
    # ==========================================================

    def error(
        self,
        provider: str,
        indicator: str,
        indicator_type: str,
        error: str,
    ) -> Dict[str, Any]:

        response = self.normalize(
            provider=provider,
            indicator=indicator,
            indicator_type=indicator_type,
            response=None,
        )

        response["error"] = error

        return response


response_normalizer = ResponseNormalizer()
