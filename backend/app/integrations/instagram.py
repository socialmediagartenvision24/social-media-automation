from __future__ import annotations

import httpx

from app.integrations.base import (
    PublishResult,
    SocialPlatform,
    TokenResult,
)


class InstagramAdapter(SocialPlatform):
    """
    Instagram publishing adapter.

    The account must be an eligible Instagram professional account
    connected to the appropriate Meta assets.

    Publishing uses the official Meta Graph API.
    """

    platform = "instagram"

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
        """
        Publish an Instagram video/reel.

        This method intentionally uses the official Graph API.
        """

        try:
            async with httpx.AsyncClient(
                timeout=60.0
            ) as client:

                # ----------------------------------------------------------
                # Step 1: Create media container
                # ----------------------------------------------------------

                container_response = await client.post(
                    f"{self.base_url}/{account_id}/media",
                    params={
                        "media_type": "REELS",
                        "video_url": video_url,
                        "caption": caption or "",
                        "access_token": access_token,
                    },
                )

                container_data = (
                    container_response.json()
                )

                if (
                    container_response.status_code
                    >= 400
                ):
                    return PublishResult(
                        success=False,
                        error=(
                            container_data.get(
                                "error",
                                {},
                            ).get(
                                "message",
                                "Instagram media container failed.",
                            )
                        ),
                        raw_response=container_data,
                    )

                creation_id = container_data.get(
                    "id"
                )

                if not creation_id:
                    return PublishResult(
                        success=False,
                        error=(
                            "Instagram returned no "
                            "creation ID."
                        ),
                        raw_response=container_data,
                    )

                # ----------------------------------------------------------
                # Step 2: Wait until media is ready
                # ----------------------------------------------------------

                ready = await self._wait_for_media_ready(
                    client=client,
                    creation_id=creation_id,
                    access_token=access_token,
                )

                if not ready:
                    return PublishResult(
                        success=False,
                        error=(
                            "Instagram media was not "
                            "ready for publishing."
                        ),
                    )

                # ----------------------------------------------------------
                # Step 3: Publish container
                # ----------------------------------------------------------

                publish_response = await client.post(
                    f"{self.base_url}/{account_id}/media_publish",
                    params={
                        "creation_id": creation_id,
                        "access_token": access_token,
                    },
                )

                publish_data = (
                    publish_response.json()
                )

                if (
                    publish_response.status_code
                    >= 400
                ):
                    return PublishResult(
                        success=False,
                        error=(
                            publish_data.get(
                                "error",
                                {},
                            ).get(
                                "message",
                                "Instagram publishing failed.",
                            )
                        ),
                        raw_response=publish_data,
                    )

                return PublishResult(
                    success=True,
                    external_post_id=publish_data.get(
                        "id"
                    ),
                    raw_response=publish_data,
                )

        except httpx.HTTPError as exc:
            return PublishResult(
                success=False,
                error=f"Instagram HTTP error: {exc}",
            )

        except Exception as exc:
            return PublishResult(
                success=False,
                error=f"Instagram error: {exc}",
            )

    async def _wait_for_media_ready(
        self,
        *,
        client: httpx.AsyncClient,
        creation_id: str,
        access_token: str,
        max_attempts: int = 20,
        delay_seconds: int = 5,
    ) -> bool:
        """
        Poll Instagram until the media container is ready.

        This prevents publishing immediately after the upload
        when Instagram is still processing the video.
        """

        import asyncio

        for _ in range(max_attempts):

            response = await client.get(
                f"{self.base_url}/{creation_id}",
                params={
                    "fields": "status_code",
                    "access_token": access_token,
                },
            )

            data = response.json()

            if response.status_code >= 400:
                return False

            status_code = data.get(
                "status_code"
            )

            if status_code == "FINISHED":
                return True

            if status_code in {
                "ERROR",
                "EXPIRED",
            }:
                return False

            await asyncio.sleep(
                delay_seconds
            )

        return False

    async def refresh_access_token(
        self,
        *,
        refresh_token: str,
    ) -> TokenResult:
        """
        Instagram/Meta token refresh is handled through
        the Meta OAuth token flow.

        The exact OAuth credentials are supplied by the
        application configuration.
        """

        return TokenResult(
            success=False,
            error=(
                "Instagram token refresh is handled "
                "through the Meta OAuth service."
            ),
        )
