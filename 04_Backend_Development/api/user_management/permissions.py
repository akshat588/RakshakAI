"""
RakshakAI v2
Permissions

Permission validation engine.
"""

from __future__ import annotations

from typing import List

from .roles import roles


class Permissions:
    """
    Permission checker.
    """

    def __init__(self) -> None:

        self.roles = roles

    # ==========================================================
    # Check Permission
    # ==========================================================

    def has_permission(
        self,
        role: str,
        permission: str,
    ) -> bool:

        return permission in self.roles.get(role)

    # ==========================================================
    # Check Multiple Permissions
    # ==========================================================

    def has_all(
        self,
        role: str,
        permissions: List[str],
    ) -> bool:

        role_permissions = set(self.roles.get(role))

        return all(permission in role_permissions for permission in permissions)

    # ==========================================================
    # Check Any Permission
    # ==========================================================

    def has_any(
        self,
        role: str,
        permissions: List[str],
    ) -> bool:

        role_permissions = set(self.roles.get(role))

        return any(permission in role_permissions for permission in permissions)


permissions = Permissions()
