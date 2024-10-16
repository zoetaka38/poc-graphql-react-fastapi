import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, extra="allow"):
    PROJECT_TITLE: str = "Fast Api GraphQL Strawberry"
    PROJECT_VERSION: str = "0.0.1"
    BASE_URL: str = "http://0.0.0.0:80"
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"config/{os.environ['APP_CONFIG_FILE']}.env",
        case_sensitive=True,
    )


settings = Settings()
