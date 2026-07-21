"""
RakshakAI v2
Provider Manager

Central manager for all external threat intelligence providers.
"""

from __future__ import annotations

from typing import Any, Dict, List


class ProviderManager:
    """
    Registers and manages external threat intelligence providers.
    """

    def __init__(self) -> None:

        self.providers: Dict[str, Any] = {}

    # ==========================================================
    # Register Provider
    # ==========================================================

    def register(
        self,
        provider: Any,
    ) -> None:

        self.providers[provider.provider_name] = provider

    # ==========================================================
    # Get Provider
    # ==========================================================

    def get(
        self,
        provider_name: str,
    ) -> Any:

        return self.providers.get(provider_name)

    # ==========================================================
    # List Providers
    # ==========================================================

    def list(self) -> List[str]:

        return sorted(self.providers.keys())

    # ==========================================================
    # Health
    # ==========================================================

    def health(self) -> List[Dict[str, Any]]:

        return [provider.health() for provider in self.providers.values()]

    # ==========================================================
    # Lookup
    # ==========================================================

    def lookup(
        self,
        indicator: str,
    ) -> Dict[str, Dict[str, Any]]:

        results = {}

        for name, provider in self.providers.items():

            if not provider.is_enabled():
                continue

            results[name] = provider.lookup(indicator)

        return results


provider_manager = ProviderManager()
