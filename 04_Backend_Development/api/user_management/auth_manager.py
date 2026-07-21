"""
RakshakAI v2
Authentication Manager

Provides authentication services for the user management module.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .session_manager import session_manager
from .user_manager import user_manager
from .permissions import permissions


class AuthManager:
    """
    Authentication service.
    """

    def __init__(self) -> None:

        self.user_manager = user_manager
        self.session_manager = session_manager
        self.permissions = permissions

    # ==========================================================
    # Login
    # ==========================================================

    def login(
        self,
        username: str,
    ) -> Optional[Dict[str, Any]]:

        user = self.user_manager.get(username)

        if user is None:
            return None

        if not user.get("active", True):
            return None

        session = self.session_manager.create(username)

        return {
            "authenticated": True,
            "user": user,
            "session": session,
        }

    # ==========================================================
    # Logout
    # ==========================================================

    def logout(
        self,
        session_id: str,
    ) -> bool:

        return self.session_manager.end(session_id)

    # ==========================================================
    # Validate Session
    # ==========================================================

    def validate(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:

        return self.session_manager.get(session_id)

    # ==========================================================
    # Permission Check
    # ==========================================================

    def has_permission(
        self,
        username: str,
        permission: str,
    ) -> bool:

        user = self.user_manager.get(username)

        if user is None:
            return False

        return self.permissions.has_permission(
            user.get("role", "viewer"),
            permission,
        )


auth_manager = AuthManager()
