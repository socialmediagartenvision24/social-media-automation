from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
)

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)


@router.get("")
async def list_campaigns(
    current_user: dict = Depends(get_current_user),
):
    return {
        "items": [],
    }


@router.post("")
async def create_campaign(
    payload: CampaignCreate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Campaign-Erstellung wird im nächsten API-Schritt angeschlossen.",
        "data": payload.model_dump(),
    }


@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "campaign_id": campaign_id,
    }


@router.patch("/{campaign_id}")
async def update_campaign(
    campaign_id: str,
    payload: CampaignUpdate,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Campaign-Update wird im nächsten API-Schritt angeschlossen.",
        "campaign_id": campaign_id,
        "data": payload.model_dump(exclude_unset=True),
    }


@router.post("/{campaign_id}/activate")
async def activate_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Campaign-Aktivierung wird im Scheduler-Schritt angeschlossen.",
        "campaign_id": campaign_id,
    }


@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Campaign-Pause wird im Scheduler-Schritt angeschlossen.",
        "campaign_id": campaign_id,
    }
