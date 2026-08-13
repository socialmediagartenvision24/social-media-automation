from __future__ import annotations

import httpx

from app.integrations.base import (
    PublishResult,
    SocialPlatform,
    TokenResult,
)


class FacebookAdapter(SocialPlatform):
    """
    Facebook video publishing adapter.

    Uses the official Meta Graph API.
    """

    platform = "facebook"

    GRAPH_API_BASE = "https://graph.facebook.com"

    def __init__(
        self,
        api_version: str = "v23.0",
    ):
        self.api_version = api_version

    @property
    def base_url(self) -> str:
        return (
            f"{self.GRAPH_API_BASE}/"
            f"{self.api_version}"
        )

    async def publish_video(
        self,
        *,
        access_token: str,
        account_id: str,
        video_url: str,
        caption: str | None = None,
    ) -> PublishResult:

        try:
            async with httpx.AsyncClient(
                timeout=120.0
            ) as client:

                response = await client.post(
                    f"{self.base_url}/{account_id}/videos",
                    params={
                        "file_url": video_url,
                        "description": caption or "",
                        "access_token": access_token,
                    },
                )

                data = response.json()

                if response.status_code >= 400:
                    return PublishResult(
                        success=False,
                        error=(
                            data.get(
                                "error",
                                {},
                            ).get(
                                "message",
                                "Facebook publishing failed.",
                            )
                        ),
                        raw_response=data,
                    )

                return PublishResult(
                    success=True,
                    external_post_id=data.get(
                        "id"
                    ),
                    raw_response=data,
                )

        except httpx.HTTPError as exc:
            return PublishResult(
                success=False,
                error=f"Facebook HTTP error: {exc}",
            )

        except Exception as exc:
            return PublishResult(
                success=False,
                error=f"Facebook error: {exc}",
            )

    async def refresh_access_token(
        self,
        *,
        refresh_token: str,
    ) -> TokenResult:
        return TokenResult(
            success=False,
            error=(
                "Facebook token refresh is handled "
                "through the Meta OAuth service."
            ),
        )
