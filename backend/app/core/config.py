from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Social Media Automation API"
    app_version: str = "1.0.0"

    environment: str = "development"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    supabase_url: str
    supabase_service_role_key: str

    frontend_url: str = "http://localhost:3000"

    jwt_secret: str = ""

    scheduler_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
