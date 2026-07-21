"""
RakshakAI v2
Case Bookmarks

Manages bookmarked investigation cases.
"""

from __future__ import annotations

from typing import Dict, List


class Bookmarks:
    """
    Bookmark manager for investigation cases.
    """

    def __init__(self) -> None:

        self._bookmarks: set[str] = set()

    # ==========================================================
    # Add Bookmark
    # ==========================================================

    def add(
        self,
        case_id: str,
    ) -> bool:

        self._bookmarks.add(case_id)

        return True

    # ==========================================================
    # Remove Bookmark
    # ==========================================================

    def remove(
        self,
        case_id: str,
    ) -> bool:

        if case_id not in self._bookmarks:
            return False

        self._bookmarks.remove(case_id)

        return True

    # ==========================================================
    # Check Bookmark
    # ==========================================================

    def exists(
        self,
        case_id: str,
    ) -> bool:

        return case_id in self._bookmarks

    # ==========================================================
    # List Bookmarks
    # ==========================================================

    def list(self) -> List[str]:

        return sorted(self._bookmarks)

    # ==========================================================
    # Count
    # ==========================================================

    def count(self) -> int:

        return len(self._bookmarks)

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self) -> None:

        self._bookmarks.clear()


bookmarks = Bookmarks()
