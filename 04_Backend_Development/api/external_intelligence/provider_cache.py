"""
RakshakAI v2
Provider Cache

Simple in-memory cache for external threat intelligence providers.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional


class ProviderCache:
    """
    In-memory cache with TTL support.
    """

    def __init__(
        self,
        ttl: int = 3600,
    ) -> None:

        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Cache Key
    # ==========================================================

    @staticmethod
    def _key(
        provider: str,
        indicator: str,
    ) -> str:

        return f"{provider}:{indicator.lower().strip()}"

    # ==========================================================
    # Get
    # ==========================================================

    def get(
        self,
        provider: str,
        indicator: str,
    ) -> Optional[Dict[str, Any]]:

        key = self._key(provider, indicator)

        item = self._cache.get(key)

        if not item:
            return None

        if time.time() > item["expires_at"]:
            del self._cache[key]
            return None

        return item["data"]

    # ==========================================================
    # Set
    # ==========================================================

    def set(
        self,
        provider: str,
        indicator: str,
        data: Dict[str, Any],
    ) -> None:

        key = self._key(provider, indicator)

        self._cache[key] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
        }

    # ==========================================================
    # Remove
    # ==========================================================

    def remove(
        self,
        provider: str,
        indicator: str,
    ) -> bool:

        key = self._key(provider, indicator)

        if key in self._cache:
            del self._cache[key]
            return True

        return False

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self) -> None:

        self._cache.clear()

    # ==========================================================
    # Statistics
    # ==========================================================

    def statistics(self) -> Dict[str, Any]:

        valid = 0

        for item in self._cache.values():
            if time.time() <= item["expires_at"]:
                valid += 1

        return {
            "entries": len(self._cache),
            "valid_entries": valid,
            "ttl_seconds": self.ttl,
        }


provider_cache = ProviderCache()
