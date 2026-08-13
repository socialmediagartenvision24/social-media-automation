from __future__ import annotations

import time
from urllib.parse import urlencode

import httpx

from app.core.config import settings
from app.oauth.base import OAuthResult, OAuthToken


class TikTokOAuth:
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
    TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

    def authorization_url(
        self,
        *,
        state: str,
    ) -> str:

        params = {
            "client_key": settings.tiktok_client_key,
            "scope": settings.tiktok_scopes,
            "response_type": "code",
            "redirect_uri": settings.tiktok_redirect_uri,
            "state": state,
        }

        return (
            f"{self.AUTH_URL}?"
            f"{urlencode(params)}"
        )

    async def exchange_code(
        self,
        *,
        code: str,
    ) -> OAuthResult:

        try:
            async with httpx.AsyncClient(
                timeout=30.0
            ) as client:

                response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_key": settings.tiktok_client_key,
                        "client_secret": settings.tiktok_client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": settings.tiktok_redirect_uri,
                    },
                    headers={
                        "Content-Type": (
                            "application/x-www-form-urlencoded"
                        ),
                    },
                )

                data = response.json()

                if response.status_code >= 400:
                    return OAuthResult(
                        success=False,
                        error=data.get(
                            "error_description"
                        ) or data.get(
                            "error"
                        ) or "TikTok OAuth failed.",
                        raw_response=data,
                    )

                expires_in = data.get(
                    "expires_in"
                )

                refresh_expires_in = data.get(
                    "refresh_expires_in"
                )

                now = int(time.time())

                token = OAuthToken(
                    access_token=data["access_token"],
                    refresh_token=data.get(
                        "refresh_token"
                    ),
                    expires_at=(
                        now + int(expires_in)
                        if expires_in
                        else None
                    ),
                    refresh_expires_at=(
                        now + int(refresh_expires_in)
                        if refresh_expires_in
                        else None
                    ),
                    token_type=data.get(
                        "token_type",
                        "Bearer",
                    ),
                    scope=data.get("scope"),
                    external_user_id=data.get(
                        "open_id"
                    ),
                )

                return OAuthResult(
                    success=True,
                    token=token,
                    raw_response=data,
                )

        except httpx.HTTPError as exc:
            return OAuthResult(
                success=False,
                error=f"TikTok HTTP error: {exc}",
            )

    async def refresh_token(
        self,
        *,
        refresh_token: str,
    ) -> OAuthResult:

        try:
            async with httpx.AsyncClient(
                timeout=30.0
            ) as client:

                response = await client.post(
                    self.TOKEN_URL,
                    data={
                        "client_key": settings.tiktok_client_key,
                        "client_secret": settings.tiktok_client_secret,
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token,
                    },
                    headers={
                        "Content-Type": (
                            "application/x-www-form-urlencoded"
                        ),
                    },
                )

                data = response.json()

                if response.status_code >= 400:
                    return OAuthResult(
                        success=False,
                        error=data.get(
                            "error_description"
                        ) or data.get(
                            "error"
                        ) or "TikTok refresh failed.",
                        raw_response=data,
                    )

                now = int(time.time())

                expires_in = data.get(
                    "expires_in"
                )

                refresh_expires_in = data.get(
                    "refresh_expires_in"
                )

                token = OAuthToken(
                    access_token=data["access_token"],
                    refresh_token=data.get(
                        "refresh_token",
                        refresh_token,
                    ),
                    expires_at=(
                        now + int(expires_in)
                        if expires_in
                        else None
                    ),
                    refresh_expires_at=(
                        now + int(refresh_expires_in)
                        if refresh_expires_in
                        else None
                    ),
                    token_type=data.get(
                        "token_type",
                        "Bearer",
                    ),
                    scope=data.get("scope"),
                    external_user_id=data.get(
                        "open_id"
                    ),
                )

                return OAuthResult(
                    success=True,
                    token=token,
                    raw_response=data,
                )

        except httpx.HTTPError as exc:
            return OAuthResult(
                success=False,
                error=f"TikTok HTTP error: {exc}",
            )
