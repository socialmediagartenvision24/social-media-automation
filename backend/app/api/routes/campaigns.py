from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
)
from app.services.campaign_scheduler import (
    generate_campaign_posts,
)
from app.services.supabase import get_supabase_admin


router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)


@router.get("")
async def list_campaigns(
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("campaigns")
        .select("*")
        .eq("user_id", current_user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "items": result.data or [],
    }


@router.post("")
async def create_campaign(
    payload: CampaignCreate,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    schedule = payload.schedule

    campaign_data = {
        "user_id": current_user["id"],
        "name": payload.name,
        "description": payload.description,
        "status": "draft",
        "timezone": schedule.timezone,
        "start_date": schedule.start_date.isoformat(),
        "end_date": (
            schedule.end_date.isoformat()
            if schedule.end_date
            else None
        ),
        "posts_per_day": schedule.posts_per_day,
        "schedule_mode": schedule.schedule_mode,
        "interval_minutes": schedule.interval_minutes,
        "posting_times": schedule.posting_times,
        "repeat_enabled": schedule.repeat_enabled,
        "repeat_interval_days": schedule.repeat_interval_days,
    }

    campaign_result = (
        supabase
        .table("campaigns")
        .insert(campaign_data)
        .execute()
    )

    if not campaign_result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kampagne konnte nicht erstellt werden.",
        )

    campaign = campaign_result.data[0]

    campaign_id = campaign["id"]

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    if payload.account_ids:

        accounts_result = (
            supabase
            .table("social_accounts")
            .select("id")
            .in_("id", payload.account_ids)
            .eq("user_id", current_user["id"])
            .execute()
        )

        valid_account_ids = {
            account["id"]
            for account in (
                accounts_result.data or []
            )
        }

        account_rows = [
            {
                "campaign_id": campaign_id,
                "account_id": account_id,
                "enabled": True,
            }
            for account_id in payload.account_ids
            if account_id in valid_account_ids
        ]

        if account_rows:
            supabase.table(
                "campaign_accounts"
            ).insert(account_rows).execute()

    # ------------------------------------------------------------------
    # Videos
    # ------------------------------------------------------------------

    if payload.video_ids:

        videos_result = (
            supabase
            .table("videos")
            .select("id")
            .in_("id", payload.video_ids)
            .eq("user_id", current_user["id"])
            .execute()
        )

        valid_video_ids = {
            video["id"]
            for video in (
                videos_result.data or []
            )
        }

        video_rows = [
            {
                "campaign_id": campaign_id,
                "video_id": video_id,
                "position": index + 1,
                "enabled": True,
            }
            for index, video_id in enumerate(
                payload.video_ids
            )
            if video_id in valid_video_ids
        ]

        if video_rows:
            supabase.table(
                "campaign_videos"
            ).insert(video_rows).execute()

    return campaign


@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("campaigns")
        .select("*")
        .eq("id", campaign_id)
        .eq("user_id", current_user["id"])
        .maybe_single()
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kampagne nicht gefunden.",
        )

    return result.data


@router.patch("/{campaign_id}")
async def update_campaign(
    campaign_id: str,
    payload: CampaignUpdate,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    update_data = {}

    if payload.name is not None:
        update_data["name"] = payload.name

    if payload.description is not None:
        update_data["description"] = payload.description

    if payload.status is not None:
        update_data["status"] = payload.status

    if payload.schedule is not None:

        schedule = payload.schedule

        update_data.update(
            {
                "timezone": schedule.timezone,
                "start_date": schedule.start_date.isoformat(),
                "end_date": (
                    schedule.end_date.isoformat()
                    if schedule.end_date
                    else None
                ),
                "posts_per_day": schedule.posts_per_day,
                "schedule_mode": schedule.schedule_mode,
                "interval_minutes": schedule.interval_minutes,
                "posting_times": schedule.posting_times,
                "repeat_enabled": schedule.repeat_enabled,
                "repeat_interval_days": (
                    schedule.repeat_interval_days
                ),
            }
        )

    if update_data:

        result = (
            supabase
            .table("campaigns")
            .update(update_data)
            .eq("id", campaign_id)
            .eq("user_id", current_user["id"])
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kampagne nicht gefunden.",
            )

    if payload.account_ids is not None:

        accounts_result = (
            supabase
            .table("social_accounts")
            .select("id")
            .in_("id", payload.account_ids)
            .eq("user_id", current_user["id"])
            .execute()
        )

        valid_account_ids = {
            account["id"]
            for account in (
                accounts_result.data or []
            )
        }

        supabase.table(
            "campaign_accounts"
        ).delete().eq(
            "campaign_id",
            campaign_id,
        ).execute()

        rows = [
            {
                "campaign_id": campaign_id,
                "account_id": account_id,
                "enabled": True,
            }
            for account_id in payload.account_ids
            if account_id in valid_account_ids
        ]

        if rows:
            supabase.table(
                "campaign_accounts"
            ).insert(rows).execute()

    if payload.video_ids is not None:

        videos_result = (
            supabase
            .table("videos")
            .select("id")
            .in_("id", payload.video_ids)
            .eq("user_id", current_user["id"])
            .execute()
        )

        valid_video_ids = {
            video["id"]
            for video in (
                videos_result.data or []
            )
        }

        supabase.table(
            "campaign_videos"
        ).delete().eq(
            "campaign_id",
            campaign_id,
        ).execute()

        rows = [
            {
                "campaign_id": campaign_id,
                "video_id": video_id,
                "position": index + 1,
                "enabled": True,
            }
            for index, video_id in enumerate(
                payload.video_ids
            )
            if video_id in valid_video_ids
        ]

        if rows:
            supabase.table(
                "campaign_videos"
            ).insert(rows).execute()

    result = (
        supabase
        .table("campaigns")
        .select("*")
        .eq("id", campaign_id)
        .eq("user_id", current_user["id"])
        .single()
        .execute()
    )

    return result.data


@router.post("/{campaign_id}/generate")
async def generate_posts(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate the actual post queue for a campaign.
    """

    posts = await generate_campaign_posts(
        campaign_id=campaign_id,
        user_id=current_user["id"],
    )

    return {
        "success": True,
        "generated": len(posts),
        "posts": posts,
    }


@router.post("/{campaign_id}/activate")
async def activate_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    # First generate posts.
    posts = await generate_campaign_posts(
        campaign_id=campaign_id,
        user_id=current_user["id"],
    )

    result = (
        supabase
        .table("campaigns")
        .update(
            {
                "status": "active",
            }
        )
        .eq("id", campaign_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kampagne nicht gefunden.",
        )

    return {
        "success": True,
        "campaign": result.data[0],
        "generated_posts": len(posts),
    }


@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("campaigns")
        .update(
            {
                "status": "paused",
            }
        )
        .eq("id", campaign_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kampagne nicht gefunden.",
        )

    return {
        "success": True,
        "campaign": result.data[0],
    }
