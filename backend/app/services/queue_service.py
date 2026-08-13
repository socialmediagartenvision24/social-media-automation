from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from app.services.supabase import get_supabase_admin


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def enqueue_due_posts(
    limit: int = 100,
) -> list[dict[str, Any]]:
    """
    Find scheduled posts whose scheduled_at has arrived
    and atomically move them to the publishing queue.

    The actual publishing is handled by the worker.
    """

    supabase = get_supabase_admin()

    now = _now_iso()

    result = (
        supabase
        .table("posts")
        .select("*")
        .eq("status", "scheduled")
        .lte("scheduled_at", now)
        .order("scheduled_at")
        .limit(limit)
        .execute()
    )

    posts = result.data or []

    if not posts:
        return []

    queued: list[dict[str, Any]] = []

    for post in posts:
        post_id = post["id"]

        update = (
            supabase
            .table("posts")
            .update(
                {
                    "status": "queued",
                    "queued_at": now,
                }
            )
            .eq("id", post_id)
            .eq("status", "scheduled")
            .execute()
        )

        if update.data:
            queued.extend(update.data)

    return queued


async def get_queue(
    user_id: str,
    limit: int = 100,
) -> list[dict[str, Any]]:
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("posts")
        .select(
            """
            id,
            campaign_id,
            account_id,
            video_id,
            platform,
            status,
            scheduled_at,
            queued_at,
            published_at,
            retry_count,
            max_retries,
            error_message,
            created_at
            """
        )
        .eq("user_id", user_id)
        .in_(
            "status",
            [
                "queued",
                "publishing",
                "failed",
            ],
        )
        .order("scheduled_at")
        .limit(limit)
        .execute()
    )

    return result.data or []


async def retry_post(
    post_id: str,
    user_id: str,
) -> dict[str, Any]:
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("posts")
        .update(
            {
                "status": "queued",
                "error_message": None,
            }
        )
        .eq("id", post_id)
        .eq("user_id", user_id)
        .eq("status", "failed")
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fehlgeschlagener Post wurde nicht gefunden.",
        )

    return result.data[0]


async def cancel_post(
    post_id: str,
    user_id: str,
) -> dict[str, Any]:
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("posts")
        .update(
            {
                "status": "cancelled",
            }
        )
        .eq("id", post_id)
        .eq("user_id", user_id)
        .in_(
            "status",
            [
                "scheduled",
                "queued",
            ],
        )
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post kann nicht mehr abgebrochen werden.",
        )

    return result.data[0]
