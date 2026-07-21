"""
RakshakAI v2
Profile Manager

Manages user profile information.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Optional

from .user_manager import user_manager


class ProfileManager:
    """
    User profile manager.
    """

    def __init__(self) -> None:

        self.user_manager = user_manager

    # ==========================================================
    # Get Profile
    # ==========================================================

    def get_profile(
        self,
        username: str,
    ) -> Optional[Dict[str, Any]]:

        return self.user_manager.get(username)

    # ==========================================================
    # Update Profile
    # ==========================================================

    def update_profile(
        self,
        username: str,
        updates: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:

        user = self.user_manager._users.get(username)

        if user is None:
            return None

        user.update(updates)

        return deepcopy(user)


profile_manager = ProfileManager()
