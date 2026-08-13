from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


@lru_cache
def get_supabase_admin() -> Client:
    """
    Server-side Supabase client.

    This client uses the Service Role Key and MUST NEVER be exposed
    to the frontend.
    """

    return create_client(
        settings.supabase_url,
        settings.supabase_service_role_key,
    )
