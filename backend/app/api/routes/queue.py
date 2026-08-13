from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_user
from app.services.queue_service import (
    cancel_post,
    get_queue,
    retry_post,
)


router = APIRouter(
    prefix="/queue",
    tags=["Queue"],
)


@router.get("")
async def list_queue(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(
        default=100,
        ge=1,
        le=500,
    ),
):
    posts = await get_queue(
        user_id=current_user["id"],
        limit=limit,
    )

    return {
        "items": posts,
        "count": len(posts),
    }


@router.post("/{post_id}/retry")
async def retry_queue_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    post = await retry_post(
        post_id=post_id,
        user_id=current_user["id"],
    )

    return {
        "success": True,
        "post": post,
    }


@router.post("/{post_id}/cancel")
async def cancel_queue_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    post = await cancel_post(
        post_id=post_id,
        user_id=current_user["id"],
    )

    return {
        "success": True,
        "post": post,
    }
