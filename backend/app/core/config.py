from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    api_v1_prefix: str = "/api"
    cors_origins: str = "http://localhost:5173"
    environment: str = "development"
    database_url: str = "sqlite:///./data/app.db"
    git_sha: str | None = None  # CI から注入可能 (例: GITHUB_SHA)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # 大文字/小文字どちらの環境変数名でも可


@lru_cache
def get_settings() -> Settings:
    return Settings()
