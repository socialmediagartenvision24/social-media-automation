from fastapi import HTTPException, status

from app.services.supabase import get_supabase_admin


def get_profile(user_id: str) -> dict:
    supabase = get_supabase_admin()

    result = (
        supabase
        .table("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User-Profil wurde nicht gefunden.",
        )

    return result.data
