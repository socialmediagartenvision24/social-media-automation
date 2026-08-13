from fastapi import APIRouter, Depends

from app.core.security import get_current_user

router = APIRouter(
    prefix="/queue",
    tags=["Queue"],
)


@router.get("")
async def get_queue(
    current_user: dict = Depends(get_current_user),
):
    return {
        "items": [],
    }


@router.get("/stats")
async def get_queue_stats(
    current_user: dict = Depends(get_current_user),
):
    return {
        "pending": 0,
        "processing": 0,
        "scheduled": 0,
        "published": 0,
        "failed": 0,
        "cancelled": 0,
    }
