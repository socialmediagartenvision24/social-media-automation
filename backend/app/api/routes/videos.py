from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.video import VideoCreate

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.get("")
async def list_videos(
    current_user: dict = Depends(get_current_user),
):
    return {
        "items": [],
    }


@router.post("")
async def create_video(
    payload: VideoCreate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Video-Erstellung wird im nächsten API-Schritt angeschlossen.",
        "data": payload.model_dump(),
    }


@router.delete("/{video_id}")
async def delete_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Video-Löschung wird im nächsten API-Schritt angeschlossen.",
        "video_id": video_id,
    }
