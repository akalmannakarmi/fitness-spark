from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongo_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_auth"
    secret_key: str = ""
    cors_origins: str = "http://localhost:3000"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    auth_prefix: str = "/auth"
    stats_prefix: str = "/stats"
    admin_prefix: str = "/admin"
    apiv1_prefix: str = "/api/v1"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin]


settings = Settings()

if not settings.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is required")

MONGO_URL = settings.mongo_url
DATABASE_NAME = settings.database_name
SECRET_KEY = settings.secret_key
CORS_ORIGINS = settings.cors_origins_list
HOST = settings.host
PORT = settings.port
RELOAD = settings.reload
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

AUTH_PREFIX = settings.auth_prefix
STATS_PREFIX = settings.stats_prefix
ADMIN_PREFIX = settings.admin_prefix
APIV1_PREFIX = settings.apiv1_prefix


class Models(StrEnum):
    User = "users"
    Stats = "statistics"
    Recipe = "recipes"
    Plans = "meal_plans"


class Actions(StrEnum):
    Create = "create"
    Read = "read"
    Update = "update"
    Delete = "delete"
