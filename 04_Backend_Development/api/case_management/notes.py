"""
RakshakAI v2
Case Notes

Stores investigation notes for individual cases.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List


class Notes:
    """
    Notes manager for investigation cases.
    """

    def __init__(self) -> None:

        self._notes: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    # ==========================================================
    # Add Note
    # ==========================================================

    def add(
        self,
        case_id: str,
        note: str,
    ) -> Dict[str, Any]:

        entry = {
            "note": note.strip(),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        self._notes[case_id].append(entry)

        return entry

    # ==========================================================
    # Get Notes
    # ==========================================================

    def get(
        self,
        case_id: str,
    ) -> List[Dict[str, Any]]:

        return list(self._notes.get(case_id, []))

    # ==========================================================
    # Delete Notes
    # ==========================================================

    def clear(
        self,
        case_id: str,
    ) -> None:

        self._notes.pop(case_id, None)

    # ==========================================================
    # Clear All
    # ==========================================================

    def clear_all(self) -> None:

        self._notes.clear()


notes = Notes()
