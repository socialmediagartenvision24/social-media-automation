from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


@lru_cache
def get_supabase_admin() -> Client:
    """
    Server-side Supabase client.

    Uses the Service Role Key.

    NEVER expose this client or key to the frontend.
    """

    if not settings.supabase_url:
        raise RuntimeError(
            "SUPABASE_URL ist nicht konfiguriert."
        )

    if not settings.supabase_service_role_key:
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY ist nicht konfiguriert."
        )

    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )
