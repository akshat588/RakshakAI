"""
RakshakAI v2
Audit Logs

Maintains an audit trail for user actions.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List


class AuditLogs:
    """
    Audit log manager.
    """

    def __init__(self) -> None:

        self._logs: List[Dict[str, Any]] = []

    # ==========================================================
    # Add Log Entry
    # ==========================================================

    def add(
        self,
        username: str,
        action: str,
        details: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "username": username,
            "action": action,
            "details": details or {},
        }

        self._logs.append(entry)

        return deepcopy(entry)

    # ==========================================================
    # Get All Logs
    # ==========================================================

    def list(
        self,
        limit: int | None = None,
    ) -> List[Dict[str, Any]]:

        logs = list(reversed(self._logs))

        if limit is not None:
            logs = logs[:limit]

        return deepcopy(logs)

    # ==========================================================
    # Clear Logs
    # ==========================================================

    def clear(self) -> None:

        self._logs.clear()


audit_logs = AuditLogs()
