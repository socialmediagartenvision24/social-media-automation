from __future__ import annotations

import httpx

from app.integrations.base import (
    PublishResult,
    SocialPlatform,
    TokenResult,
)


class TikTokAdapter(SocialPlatform):
    """
    TikTok Content Posting API adapter.

    OAuth and publishing are kept separate so that credentials
    never reach the frontend.
    """

    platform = "tiktok"

    API_BASE = "https://open.tiktokapis.com"

    def __init__(self):
        pass

    async def publish_video(
        self,
        *,
        access_token: str,
        account_id: str,
        video_url: str,
        caption: str | None = None,
    ) -> PublishResult:
        """
        TikTok publishing requires the Content Posting API flow.

        The exact publishing mode depends on the capabilities
        granted to the application/account.
        """

        if not access_token:
            return PublishResult(
                success=False,
                error="TikTok access token fehlt.",
            )

        if not account_id:
            return PublishResult(
                success=False,
                error="TikTok account ID fehlt.",
            )

        if not video_url:
            return PublishResult(
                success=False,
                error="Video URL fehlt.",
            )

        # The actual TikTok publishing flow will be implemented
        # after OAuth/account capability detection.
        return PublishResult(
            success=False,
            error=(
                "TikTok publishing adapter is not configured yet. "
                "Connect the account through OAuth first."
            ),
        )

    async def refresh_access_token(
        self,
        *,
        refresh_token: str,
    ) -> TokenResult:

        if not refresh_token:
            return TokenResult(
                success=False,
                error="TikTok refresh token fehlt.",
            )

        try:
            async with httpx.AsyncClient(
                timeout=30.0
            ) as client:

                response = await client.post(
                    f"{self.API_BASE}/v2/oauth/token/",
                    data={
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token,
                    },
                )

                data = response.json()

                if response.status_code >= 400:
                    return TokenResult(
                        success=False,
                        error=(
                            data.get(
                                "error_description"
                            )
                            or data.get("error")
                            or "TikTok token refresh failed."
                        ),
                        raw_response=data,
                    )

                return TokenResult(
                    success=True,
                    access_token=data.get(
                        "access_token"
                    ),
                    refresh_token=data.get(
                        "refresh_token"
                    ),
                    raw_response=data,
                )

        except httpx.HTTPError as exc:
            return TokenResult(
                success=False,
                error=f"TikTok HTTP error: {exc}",
            )

        except Exception as exc:
            return TokenResult(
                success=False,
                error=f"TikTok error: {exc}",
            )
