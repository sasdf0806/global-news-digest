from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql+psycopg://news_user:change_me@postgres:5432/global_news"
    pipeline_version: str = "v1"
    llm_mock_mode: bool = True
    collector_mock_mode: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
