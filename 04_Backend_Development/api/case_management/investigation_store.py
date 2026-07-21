"""
RakshakAI v2
Investigation Store

Central in-memory storage for investigation cases.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional


class InvestigationStore:
    """
    Stores investigation records.
    """

    def __init__(self) -> None:

        self._cases: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Create / Update
    # ==========================================================

    def save(
        self,
        case: Dict[str, Any],
    ) -> Dict[str, Any]:

        case_id = case.get("case_id")

        if not case_id:
            raise ValueError("case_id is required.")

        self._cases[case_id] = deepcopy(case)

        return deepcopy(case)

    # ==========================================================
    # Read
    # ==========================================================

    def get(
        self,
        case_id: str,
    ) -> Optional[Dict[str, Any]]:

        case = self._cases.get(case_id)

        if case is None:
            return None

        return deepcopy(case)

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(
        self,
        case_id: str,
    ) -> bool:

        if case_id not in self._cases:
            return False

        del self._cases[case_id]

        return True

    # ==========================================================
    # List
    # ==========================================================

    def all(self) -> List[Dict[str, Any]]:

        return [deepcopy(case) for case in self._cases.values()]

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(
        self,
        case_id: str,
    ) -> bool:

        return case_id in self._cases

    # ==========================================================
    # Count
    # ==========================================================

    def count(self) -> int:

        return len(self._cases)

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self) -> None:

        self._cases.clear()


investigation_store = InvestigationStore()
