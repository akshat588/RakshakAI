"""
RakshakAI v2
User Preferences

Stores user-specific application preferences.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict


class Preferences:
    """
    User preferences manager.
    """

    def __init__(self) -> None:

        self._preferences: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Get Preferences
    # ==========================================================

    def get(
        self,
        username: str,
    ) -> Dict[str, Any]:

        return deepcopy(self._preferences.get(username, {}))

    # ==========================================================
    # Save Preferences
    # ==========================================================

    def save(
        self,
        username: str,
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:

        self._preferences[username] = deepcopy(preferences)

        return self.get(username)

    # ==========================================================
    # Update Preferences
    # ==========================================================

    def update(
        self,
        username: str,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:

        current = self._preferences.setdefault(username, {})

        current.update(updates)

        return deepcopy(current)

    # ==========================================================
    # Remove Preferences
    # ==========================================================

    def clear(
        self,
        username: str,
    ) -> None:

        self._preferences.pop(username, None)


preferences = Preferences()
