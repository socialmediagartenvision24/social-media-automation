from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.schemas.account import (
    AccountCreate,
    AccountUpdate,
)
from app.services.supabase import get_supabase_admin


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.get("")
async def list_accounts(
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .select(
            """
            id,
            name,
            username,
            platform,
            status,
            timezone,
            profile_image_url,
            created_at,
            updated_at
            """
        )
        .eq("user_id", current_user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "items": result.data or [],
    }


@router.get("/{account_id}")
async def get_account(
    account_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .select(
            """
            id,
            name,
            username,
            platform,
            status,
            timezone,
            profile_image_url,
            created_at,
            updated_at
            """
        )
        .eq("id", account_id)
        .eq("user_id", current_user["id"])
        .maybe_single()
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account nicht gefunden.",
        )

    return result.data


@router.post("")
async def create_account(
    payload: AccountCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Creates the local account record.

    OAuth connection is intentionally handled separately.
    """

    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .insert(
            {
                "user_id": current_user["id"],
                "name": payload.name,
                "platform": payload.platform,
                "timezone": payload.timezone,
                "status": "disconnected",
            }
        )
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account konnte nicht erstellt werden.",
        )

    return result.data[0]


@router.patch("/{account_id}")
async def update_account(
    account_id: str,
    payload: AccountUpdate,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keine Änderungen angegeben.",
        )

    result = (
        supabase
        .table("social_accounts")
        .update(update_data)
        .eq("id", account_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account nicht gefunden.",
        )

    return result.data[0]


@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .delete()
        .eq("id", account_id)
        .eq("user_id", current_user["id"])
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account nicht gefunden.",
        )

    return {
        "success": True,
        "deleted_id": account_id,
    }
