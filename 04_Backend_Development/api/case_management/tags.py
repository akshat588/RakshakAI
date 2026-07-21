"""
RakshakAI v2
Case Tags

Manages tags assigned to investigation cases.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class Tags:
    """
    Tag manager for investigation cases.
    """

    def __init__(self) -> None:

        self._tags: Dict[str, List[str]] = defaultdict(list)

    # ==========================================================
    # Add Tag
    # ==========================================================

    def add(
        self,
        case_id: str,
        tag: str,
    ) -> None:

        tag = tag.strip()

        if not tag:
            return

        if tag not in self._tags[case_id]:
            self._tags[case_id].append(tag)

    # ==========================================================
    # Remove Tag
    # ==========================================================

    def remove(
        self,
        case_id: str,
        tag: str,
    ) -> bool:

        if tag not in self._tags.get(case_id, []):
            return False

        self._tags[case_id].remove(tag)
        return True

    # ==========================================================
    # Get Tags
    # ==========================================================

    def get(
        self,
        case_id: str,
    ) -> List[str]:

        return list(self._tags.get(case_id, []))

    # ==========================================================
    # All Tags
    # ==========================================================

    def all(self) -> Dict[str, List[str]]:

        return {case_id: list(tags) for case_id, tags in self._tags.items()}

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self) -> None:

        self._tags.clear()


tags = Tags()
