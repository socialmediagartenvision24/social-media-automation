from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.post import PostCreate

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("")
async def list_posts(
    current_user: dict = Depends(get_current_user),
):
    return {
        "items": [],
    }


@router.post("")
async def create_post(
    payload: PostCreate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Post-Erstellung wird im Scheduler-Schritt angeschlossen.",
        "data": payload.model_dump(mode="json"),
    }


@router.post("/{post_id}/cancel")
async def cancel_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Post-Abbruch wird im Queue-Schritt angeschlossen.",
        "post_id": post_id,
    }
