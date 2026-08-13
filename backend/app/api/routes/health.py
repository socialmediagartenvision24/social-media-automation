from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": "social-media-automation-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
