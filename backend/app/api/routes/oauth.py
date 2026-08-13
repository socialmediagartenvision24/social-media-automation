from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse

from app.core.security import get_current_user
from app.core.config import settings
from app.oauth.meta import MetaOAuth
from app.oauth.state import oauth_state_store
from app.oauth.tiktok import TikTokOAuth
from app.services.supabase import get_supabase_admin


router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"],
)


@router.get("/{platform}/connect")
async def connect_platform(
    platform: str,
    current_user: dict = Depends(get_current_user),
):
    platform = platform.lower()

    if platform not in {
        "instagram",
        "facebook",
        "tiktok",
    }:
        raise HTTPException(
            status_code=400,
            detail="Nicht unterstützte Plattform.",
        )

    state = oauth_state_store.create(
        user_id=current_user["id"],
        platform=platform,
    )

    if platform in {
        "instagram",
        "facebook",
    }:
        oauth = MetaOAuth()

    else:
        oauth = TikTokOAuth()

    return {
        "authorization_url": oauth.authorization_url(
            state=state,
        )
    }


@router.get("/{platform}/callback")
async def oauth_callback(
    platform: str,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    error_description: str | None = Query(
        default=None
    ),
):
    platform = platform.lower()

    if error:
        raise HTTPException(
            status_code=400,
            detail=error_description or error,
        )

    if not state:
        raise HTTPException(
            status_code=400,
            detail="OAuth state fehlt.",
        )

    state_data = oauth_state_store.consume(
        state,
        platform=platform,
    )

    if not state_data:
        raise HTTPException(
            status_code=400,
            detail="Ungültiger oder abgelaufener OAuth state.",
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="OAuth authorization code fehlt.",
        )

    user_id = state_data["user_id"]

    if platform in {
        "instagram",
        "facebook",
    }:
        oauth = MetaOAuth()
    else:
        oauth = TikTokOAuth()

    result = await oauth.exchange_code(
        code=code,
    )

    if not result.success or not result.token:
        raise HTTPException(
            status_code=400,
            detail=result.error or "OAuth fehlgeschlagen.",
        )

    token = result.token

    supabase = get_supabase_admin()

    account_data = {
        "user_id": user_id,
        "platform": platform,
        "external_account_id": (
            token.external_user_id
        ),
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "token_expires_at": token.expires_at,
        "refresh_token_expires_at": (
            token.refresh_expires_at
        ),
        "oauth_scope": token.scope,
        "token_type": token.token_type,
        "status": "connected",
    }

    existing = (
        supabase
        .table("social_accounts")
        .select("id")
        .eq("user_id", user_id)
        .eq("platform", platform)
        .eq(
            "external_account_id",
            token.external_user_id,
        )
        .maybe_single()
        .execute()
    )

    if existing.data:

        result_db = (
            supabase
            .table("social_accounts")
            .update(account_data)
            .eq(
                "id",
                existing.data["id"],
            )
            .execute()
        )

    else:

        result_db = (
            supabase
            .table("social_accounts")
            .insert(account_data)
            .execute()
        )

    if not result_db.data:
        raise HTTPException(
            status_code=500,
            detail=(
                "OAuth erfolgreich, aber Account "
                "konnte nicht gespeichert werden."
            ),
        )

    return RedirectResponse(
        url=(
            f"{settings.frontend_url}"
            "/dashboard/accounts"
            "?connected="
            f"{platform}"
        )
    )
