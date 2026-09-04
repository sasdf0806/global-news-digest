from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "global-news-digest"
    app_env: str = "development"
    app_timezone: str = "Asia/Shanghai"
    database_url: str = "postgresql+psycopg://news_user:change_me@postgres:5432/global_news"
    redis_url: str = "redis://redis:6379/0"
    keycloak_url: str = "http://keycloak:8080"
    keycloak_realm: str = "global-news"
    pipeline_version: str = "v1"
    llm_mock_mode: bool = True
    collector_mock_mode: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
