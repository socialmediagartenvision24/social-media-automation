from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ========================================================================
    # APPLICATION
    # ========================================================================

    app_name: str = "Social Media Automation API"
    app_version: str = "1.0.0"

    environment: str = "development"

    # ========================================================================
    # SERVER
    # ========================================================================

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # ========================================================================
    # FRONTEND
    # ========================================================================

    frontend_url: str = "http://localhost:3000"

    # ========================================================================
    # SUPABASE
    # ========================================================================

    supabase_url: str
    supabase_service_role_key: str

    # ========================================================================
    # AUTHENTICATION
    # ========================================================================

    jwt_secret: str

    # ========================================================================
    # SCHEDULER
    # ========================================================================

    scheduler_enabled: bool = True

    scheduler_interval_seconds: int = Field(
        default=30,
        ge=5,
    )

    publishing_batch_size: int = Field(
        default=10,
        ge=1,
    )

    # ========================================================================
    # PLATFORM API
    # ========================================================================

    platform_http_timeout: int = Field(
        default=30,
        ge=5,
    )

    # ========================================================================
    # META / FACEBOOK / INSTAGRAM
    # ========================================================================

    meta_app_id: str = ""
    meta_app_secret: str = ""

    meta_redirect_uri: str = (
        "http://localhost:8000/api/oauth/facebook/callback"
    )

    meta_scopes: str = ""

    # ========================================================================
    # TIKTOK
    # ========================================================================

    tiktok_client_key: str = ""
    tiktok_client_secret: str = ""

    tiktok_redirect_uri: str = (
        "http://localhost:8000/api/oauth/tiktok/callback"
    )

    tiktok_scopes: str = (
        "user.info.basic,video.publish"
    )

    # ========================================================================
    # PYDANTIC SETTINGS
    # ========================================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# ============================================================================
# SETTINGS SINGLETON
# ============================================================================

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
