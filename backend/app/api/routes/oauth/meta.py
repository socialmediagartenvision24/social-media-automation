from __future__ import annotations

from urllib.parse import urlencode

import httpx

from app.core.config import settings
from app.oauth.base import OAuthResult, OAuthToken


class MetaOAuth:
    """
    OAuth foundation for Meta integrations.

    Instagram and Facebook account discovery/publishing are
    implemented separately because the required assets and
    permissions differ.
    """

    AUTH_URL = "https://www.facebook.com/v23.0/dialog/oauth"
    TOKEN_URL = "https://graph.facebook.com/v23.0/oauth/access_token"

    def authorization_url(
        self,
        *,
        state: str,
    ) -> str:

        params = {
            "client_id": settings.meta_app_id,
            "redirect_uri": settings.meta_redirect_uri,
            "state": state,
            "response_type": "code",
            "scope": settings.meta_scopes,
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

                response = await client.get(
                    self.TOKEN_URL,
                    params={
                        "client_id": settings.meta_app_id,
                        "client_secret": (
                            settings.meta_app_secret
                        ),
                        "redirect_uri": (
                            settings.meta_redirect_uri
                        ),
                        "code": code,
                    },
                )

                data = response.json()

                if response.status_code >= 400:
                    return OAuthResult(
                        success=False,
                        error=data.get(
                            "error",
                            {},
                        ).get(
                            "message",
                            "Meta OAuth failed.",
                        ),
                        raw_response=data,
                    )

                access_token = data.get(
                    "access_token"
                )

                if not access_token:
                    return OAuthResult(
                        success=False,
                        error=(
                            "Meta returned no access token."
                        ),
                        raw_response=data,
                    )

                return OAuthResult(
                    success=True,
                    token=OAuthToken(
                        access_token=access_token,
                        token_type=data.get(
                            "token_type",
                            "Bearer",
                        ),
                    ),
                    raw_response=data,
                )

        except httpx.HTTPError as exc:
            return OAuthResult(
                success=False,
                error=f"Meta HTTP error: {exc}",
            )
