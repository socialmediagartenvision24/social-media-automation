from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.schemas.video import VideoCreate
from app.services.supabase import get_supabase_admin


router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.get("")
async def list_videos(
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("videos")
        .select("*")
        .eq("user_id", current_user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "items": result.data or [],
    }


@router.get("/{video_id}")
async def get_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("videos")
        .select("*")
        .eq("id", video_id)
        .eq("user_id", current_user["id"])
        .maybe_single()
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video nicht gefunden.",
        )

    return result.data


@router.post("")
async def create_video(
    payload: VideoCreate,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("videos")
        .insert(
            {
                "user_id": current_user["id"],
                "name": payload.name,
                "description": payload.description,
                "storage_path": payload.storage_path,
                "mime_type": payload.mime_type,
                "file_size_bytes": payload.file_size_bytes,
                "status": "uploading",
            }
        )
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video konnte nicht erstellt werden.",
        )

    return result.data[0]


@router.delete("/{video_id}")
async def delete_video(
    video_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("videos")
        .update(
            {
                "status": "deleted",
            }
        )
        .eq("id", video_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video nicht gefunden.",
        )

    return {
        "success": True,
        "deleted_id": video_id,
    }
