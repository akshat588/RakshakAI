"""
RakshakAI v2
Base External Threat Intelligence Provider

Abstract base class for all external threat intelligence providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseThreatProvider(ABC):
    """
    Base class for every external intelligence provider.
    """

    def __init__(
        self,
        provider_name: str,
        enabled: bool = True,
        timeout: int = 10,
    ) -> None:

        self.provider_name = provider_name
        self.enabled = enabled
        self.timeout = timeout

    # ==========================================================
    # Provider Information
    # ==========================================================

    def metadata(self) -> Dict[str, Any]:

        return {
            "provider": self.provider_name,
            "enabled": self.enabled,
            "timeout": self.timeout,
        }

    # ==========================================================
    # Availability
    # ==========================================================

    def is_enabled(self) -> bool:

        return self.enabled

    # ==========================================================
    # Enable / Disable
    # ==========================================================

    def enable(self) -> None:

        self.enabled = True

    def disable(self) -> None:

        self.enabled = False

    # ==========================================================
    # Health
    # ==========================================================

    def health(self) -> Dict[str, Any]:

        return {
            "provider": self.provider_name,
            "enabled": self.enabled,
            "status": "available" if self.enabled else "disabled",
        }

    # ==========================================================
    # Abstract Lookup
    # ==========================================================

    @abstractmethod
    def lookup(
        self,
        indicator: str,
    ) -> Dict[str, Any]:
        """
        Perform reputation lookup.
        """
        raise NotImplementedError

    # ==========================================================
    # Default Empty Response
    # ==========================================================

    def empty_response(
        self,
        indicator: str,
    ) -> Dict[str, Any]:

        return {
            "provider": self.provider_name,
            "indicator": indicator,
            "found": False,
            "risk": "unknown",
            "confidence": 0,
            "category": None,
            "details": {},
        }
