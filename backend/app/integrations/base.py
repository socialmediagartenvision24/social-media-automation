from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class PublishResult:
    success: bool
    external_post_id: str | None = None
    error: str | None = None
    raw_response: dict[str, Any] | None = None


class SocialPlatform(ABC):

    @abstractmethod
    async def publish_video(
        self,
        *,
        access_token: str,
        account_id: str,
        video_url: str,
        caption: str | None = None,
    ) -> PublishResult:
        raise NotImplementedError

    @abstractmethod
    async def refresh_access_token(
        self,
        *,
        refresh_token: str,
    ) -> dict[str, Any]:
        raise NotImplementedError
