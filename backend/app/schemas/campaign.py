from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


CampaignStatus = Literal[
    "draft",
    "active",
    "paused",
    "completed",
    "archived",
]


ScheduleMode = Literal[
    "fixed",
    "interval",
]


class CampaignSchedule(BaseModel):
    timezone: str = "Europe/Berlin"

    start_date: date

    end_date: date | None = None

    posts_per_day: int = Field(
        default=1,
        ge=1,
    )

    schedule_mode: ScheduleMode = "fixed"

    interval_minutes: int | None = Field(
        default=None,
        gt=0,
    )

    posting_times: list[str] = Field(
        default_factory=list,
    )

    repeat_enabled: bool = False

    repeat_interval_days: int | None = Field(
        default=None,
        gt=0,
    )


class CampaignCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str | None = None

    account_ids: list[str] = Field(
        default_factory=list,
    )

    video_ids: list[str] = Field(
        default_factory=list,
    )

    schedule: CampaignSchedule


class CampaignUpdate(BaseModel):
    name: str | None = None

    description: str | None = None

    status: CampaignStatus | None = None

    account_ids: list[str] | None = None

    video_ids: list[str] | None = None

    schedule: CampaignSchedule | None = None


class CampaignResponse(BaseModel):
    id: str

    name: str

    description: str | None

    status: CampaignStatus

    timezone: str

    start_date: date

    end_date: date | None

    posts_per_day: int

    repeat_enabled: bool

    repeat_interval_days: int | None

    created_at: datetime

    updated_at: datetime
