"""
RakshakAI v2
Roles

Defines user roles used throughout the platform.
"""

from __future__ import annotations

from typing import Dict, List


class Roles:
    """
    Role registry.
    """

    def __init__(self) -> None:

        self._roles: Dict[str, List[str]] = {
            "admin": [
                "manage_users",
                "manage_roles",
                "manage_api_keys",
                "view_dashboard",
                "view_cases",
                "export_reports",
            ],
            "analyst": [
                "view_dashboard",
                "view_cases",
                "create_cases",
                "export_reports",
            ],
            "viewer": [
                "view_dashboard",
                "view_cases",
            ],
        }

    # ==========================================================
    # Get Role
    # ==========================================================

    def get(
        self,
        role: str,
    ) -> List[str]:

        return list(self._roles.get(role, []))

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(
        self,
        role: str,
    ) -> bool:

        return role in self._roles

    # ==========================================================
    # All Roles
    # ==========================================================

    def all(self) -> Dict[str, List[str]]:

        return {role: list(permissions) for role, permissions in self._roles.items()}


roles = Roles()
