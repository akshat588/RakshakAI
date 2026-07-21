"""
RakshakAI v2
User Manager

Manages user records.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional


class UserManager:
    """
    In-memory user manager.
    """

    def __init__(self) -> None:

        self._users: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Create User
    # ==========================================================

    def create(
        self,
        username: str,
        role: str = "viewer",
    ) -> Dict[str, Any]:

        user = {
            "username": username,
            "role": role,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "active": True,
        }

        self._users[username] = user

        return deepcopy(user)

    # ==========================================================
    # Get User
    # ==========================================================

    def get(
        self,
        username: str,
    ) -> Optional[Dict[str, Any]]:

        user = self._users.get(username)

        if user is None:
            return None

        return deepcopy(user)

    # ==========================================================
    # Update Role
    # ==========================================================

    def update_role(
        self,
        username: str,
        role: str,
    ) -> bool:

        if username not in self._users:
            return False

        self._users[username]["role"] = role

        return True

    # ==========================================================
    # List Users
    # ==========================================================

    def list(self) -> List[Dict[str, Any]]:

        return [deepcopy(user) for user in self._users.values()]

    # ==========================================================
    # Delete User
    # ==========================================================

    def delete(
        self,
        username: str,
    ) -> bool:

        if username not in self._users:
            return False

        del self._users[username]

        return True


user_manager = UserManager()
