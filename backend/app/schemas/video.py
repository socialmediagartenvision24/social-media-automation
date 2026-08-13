from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


VideoStatus = Literal[
    "uploading",
    "processing",
    "ready",
    "failed",
    "deleted",
]


class VideoCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

    description: str | None = None

    storage_path: str

    mime_type: str

    file_size_bytes: int = Field(ge=0)


class VideoResponse(BaseModel):
    id: str

    name: str

    description: str | None = None

    storage_path: str

    public_url: str | None = None

    thumbnail_url: str | None = None

    mime_type: str

    file_size_bytes: int

    duration_seconds: float

    status: VideoStatus

    created_at: datetime

    updated_at: datetime
