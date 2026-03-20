from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "YouTube Partner Analytics Platform"
    frontend_url: str = "http://localhost:5173"
    database_url: str = "sqlite:///./youtube_partner.db"
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/callback"
    app_secret_key: str = "change-me"
    token_encryption_key: str = "change-me-change-me-change-me-32b"
    openai_api_key: str = ""
    youtube_api_key: str = ""
    demo_mode: bool = True

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
