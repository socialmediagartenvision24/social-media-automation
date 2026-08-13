from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


PostStatus = Literal[
    "scheduled",
    "pending",
    "processing",
    "published",
    "failed",
    "cancelled",
]


class PostCreate(BaseModel):
    campaign_id: str | None = None

    account_id: str

    video_id: str

    platform: Literal[
        "instagram",
        "facebook",
        "tiktok",
    ]

    scheduled_at: datetime

    caption: str | None = None

    max_retries: int = Field(
        default=3,
        ge=0,
    )


class PostResponse(BaseModel):
    id: str

    campaign_id: str | None

    account_id: str

    video_id: str

    platform: str

    status: PostStatus

    scheduled_at: datetime

    published_at: datetime | None

    external_post_id: str | None

    external_post_url: str | None

    error_message: str | None

    retry_count: int

    max_retries: int

    cycle_number: int

    created_at: datetime

    updated_at: datetime
