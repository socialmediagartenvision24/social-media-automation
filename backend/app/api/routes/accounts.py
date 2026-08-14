from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.schemas.account import AccountCreate, AccountUpdate
from app.services.supabase import get_supabase_admin


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


# ============================================================================
# RESPONSE FIELDS
# ============================================================================
#
# OAuth-Tokens werden ABSICHTLICH niemals über diese API zurückgegeben.
#
# access_token_encrypted
# refresh_token_encrypted
# token_expires_at
#
# bleiben ausschließlich serverseitig.
# ============================================================================

ACCOUNT_SELECT = """
    id,
    name,
    username,
    platform,
    platform_account_id,
    status,
    timezone,
    profile_image_url,
    last_synced_at,
    last_error,
    created_at,
    updated_at
"""


# ============================================================================
# LIST ACCOUNTS
# ============================================================================

@router.get("")
async def list_accounts(
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .select(ACCOUNT_SELECT)
        .eq("user_id", current_user["id"])
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "items": result.data or [],
        "count": len(result.data or []),
    }


# ============================================================================
# GET ACCOUNT
# ============================================================================

@router.get("/{account_id}")
async def get_account(
    account_id: str,
    current_user: dict = Depends(get_current_user),
):
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("social_accounts")
        .select(ACCOUNT_SELECT)
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


# ============================================================================
# CREATE ACCOUNT
# ============================================================================

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_account(
    payload: AccountCreate,
    current_user: dict = Depends(get_current_user),
):
    """
    Erstellt einen lokalen Social-Account-Eintrag.

    Die eigentliche OAuth-Verbindung zu Instagram/Facebook/TikTok
    wird separat über die jeweiligen OAuth-Flows hergestellt.
    """

    supabase = get_supabase_admin()

    insert_data = {
        "user_id": current_user["id"],
        "name": payload.name,
        "platform": payload.platform,
        "timezone": payload.timezone,
        "status": "disconnected",
    }

    result = (
        supabase
        .table("social_accounts")
        .insert(insert_data)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account konnte nicht erstellt werden.",
        )

    return result.data[0]


# ============================================================================
# UPDATE ACCOUNT
# ============================================================================

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

    # Sicherheitsmaßnahme:
    # Benutzer dürfen niemals OAuth-/Systemfelder über diesen Endpoint ändern.
    forbidden_fields = {
        "user_id",
        "platform",
        "platform_account_id",
        "access_token_encrypted",
        "refresh_token_encrypted",
        "token_expires_at",
        "status",
        "last_synced_at",
        "last_error",
    }

    blocked_fields = forbidden_fields.intersection(update_data.keys())

    if blocked_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Diese Account-Felder dürfen über diesen Endpoint "
                "nicht geändert werden."
            ),
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


# ============================================================================
# DELETE ACCOUNT
# ============================================================================

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
