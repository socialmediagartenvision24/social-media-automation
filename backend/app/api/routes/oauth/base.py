from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class OAuthToken:
    access_token: str
    refresh_token: str | None = None
    expires_at: int | None = None
    refresh_expires_at: int | None = None
    token_type: str = "Bearer"
    scope: str | None = None
    external_user_id: str | None = None


@dataclass
class OAuthResult:
    success: bool
    token: OAuthToken | None = None
    error: str | None = None
    raw_response: dict[str, Any] | None = None
