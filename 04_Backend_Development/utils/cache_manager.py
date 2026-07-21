"""
RakshakAI v2
Cache Manager
"""

from __future__ import annotations

import time
from threading import RLock
from typing import Any, Dict, Optional


class CacheManager:
    """
    Simple in-memory cache manager.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600,
    ) -> None:
        """
        Store a value with TTL.
        """

        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl,
            }

    def get(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Any:
        """
        Retrieve a cached value.
        """

        with self._lock:
            item = self._cache.get(key)

            if item is None:
                return default

            if item["expires_at"] < time.time():
                del self._cache[key]
                return default

            return item["value"]

    def exists(self, key: str) -> bool:
        """
        Check whether a key exists and is valid.
        """

        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """
        Delete a cache entry.
        """

        with self._lock:
            return self._cache.pop(key, None) is not None

    def clear(self) -> None:
        """
        Clear all cached entries.
        """

        with self._lock:
            self._cache.clear()

    def cleanup(self) -> int:
        """
        Remove expired entries.
        """

        removed = 0

        with self._lock:
            now = time.time()

            expired = [key for key, value in self._cache.items() if value["expires_at"] < now]

            for key in expired:
                del self._cache[key]
                removed += 1

        return removed

    def size(self) -> int:
        """
        Number of cached entries.
        """

        return len(self._cache)
