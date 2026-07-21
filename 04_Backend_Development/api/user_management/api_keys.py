"""
RakshakAI v2
API Keys

Manages API keys for external integrations.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


class APIKeys:
    """
    API key manager.
    """

    def __init__(self) -> None:

        self._keys: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # Create API Key
    # ==========================================================

    def create(
        self,
        name: str,
    ) -> Dict[str, Any]:

        key = {
            "id": str(uuid4()),
            "name": name,
            "key": uuid4().hex,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "active": True,
        }

        self._keys[key["id"]] = key

        return deepcopy(key)

    # ==========================================================
    # Get API Key
    # ==========================================================

    def get(
        self,
        key_id: str,
    ) -> Optional[Dict[str, Any]]:

        key = self._keys.get(key_id)

        if key is None:
            return None

        return deepcopy(key)

    # ==========================================================
    # List API Keys
    # ==========================================================

    def list(self) -> List[Dict[str, Any]]:

        return [deepcopy(key) for key in self._keys.values()]

    # ==========================================================
    # Revoke API Key
    # ==========================================================

    def revoke(
        self,
        key_id: str,
    ) -> bool:

        if key_id not in self._keys:
            return False

        self._keys[key_id]["active"] = False

        return True


api_keys = APIKeys()
