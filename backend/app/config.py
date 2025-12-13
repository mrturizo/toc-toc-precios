from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación backend."""

    app_name: str = "TocToc Precios API"
    debug: bool = True

    database_url: AnyUrl | str = "sqlite+aiosqlite:///./dev.db"

    jwt_secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


