from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# TYPES
# ============================================================================

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


# ============================================================================
# CREATE
# ============================================================================

class AccountCreate(BaseModel):
    """
    Creates a local social account record.

    OAuth credentials are NOT accepted here.
    """

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    platform: SocialPlatform

    timezone: str = Field(
        default="Europe/Berlin",
        min_length=1,
        max_length=100,
    )


# ============================================================================
# UPDATE
# ============================================================================

class AccountUpdate(BaseModel):
    """
    Fields that the user is allowed to edit manually.

    OAuth/system fields are intentionally excluded.
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    timezone: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


# ============================================================================
# RESPONSE
# ============================================================================

class AccountResponse(BaseModel):
    """
    Public account representation.

    OAuth access/refresh tokens are NEVER returned.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    name: str

    username: str | None = None

    platform: SocialPlatform

    status: AccountStatus

    timezone: str

    profile_image_url: str | None = None

    platform_account_id: str | None = None

    last_synced_at: datetime | None = None

    last_error: str | None = None

    created_at: datetime

    updated_at: datetime
