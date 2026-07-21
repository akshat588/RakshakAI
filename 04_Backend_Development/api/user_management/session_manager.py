"""
RakshakAI v2
Session Manager

Manages active user sessions.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class SessionManager:
    """
    In-memory session manager.
    """

    def __init__(self) -> None:

        self._sessions: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Create Session
    # ==========================================================

    def create(
        self,
        username: str,
    ) -> Dict[str, Any]:

        session_id = str(uuid4())

        session = {
            "session_id": session_id,
            "username": username,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "active": True,
        }

        self._sessions[session_id] = session

        return deepcopy(session)

    # ==========================================================
    # Get Session
    # ==========================================================

    def get(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:

        session = self._sessions.get(session_id)

        if session is None:
            return None

        return deepcopy(session)

    # ==========================================================
    # List Sessions
    # ==========================================================

    def list(self) -> List[Dict[str, Any]]:

        return [deepcopy(session) for session in self._sessions.values()]

    # ==========================================================
    # End Session
    # ==========================================================

    def end(
        self,
        session_id: str,
    ) -> bool:

        if session_id not in self._sessions:
            return False

        del self._sessions[session_id]

        return True

    # ==========================================================
    # Clear Sessions
    # ==========================================================

    def clear(self) -> None:

        self._sessions.clear()


session_manager = SessionManager()
