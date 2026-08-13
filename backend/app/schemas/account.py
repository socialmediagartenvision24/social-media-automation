from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


SocialPlatform = Literal[
    "instagram",
    "facebook",
    "tiktok",
]


AccountStatus = Literal[
    "connected",
    "disconnected",
    "expired",
    "error",
]


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    platform: SocialPlatform

    timezone: str = "Europe/Berlin"


class AccountUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    timezone: str | None = None


class AccountResponse(BaseModel):
    id: str

    name: str

    username: str | None = None

    platform: SocialPlatform

    status: AccountStatus

    timezone: str

    profile_image_url: str | None = None

    created_at: datetime

    updated_at: datetime
