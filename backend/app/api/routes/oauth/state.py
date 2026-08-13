from __future__ import annotations

import secrets
import time


class OAuthStateStore:
    """
    Short-lived in-memory OAuth state store.

    For a multi-instance production deployment this should later
    be moved to Redis or another shared store.
    """

    def __init__(self) -> None:
        self._states: dict[str, dict] = {}

    def create(
        self,
        *,
        user_id: str,
        platform: str,
        expires_in: int = 600,
    ) -> str:

        state = secrets.token_urlsafe(32)

        self._states[state] = {
            "user_id": user_id,
            "platform": platform,
            "expires_at": time.time() + expires_in,
        }

        return state

    def consume(
        self,
        state: str,
        *,
        platform: str,
    ) -> dict | None:

        item = self._states.pop(state, None)

        if not item:
            return None

        if item["platform"] != platform:
            return None

        if item["expires_at"] < time.time():
            return None

        return item


oauth_state_store = OAuthStateStore()
