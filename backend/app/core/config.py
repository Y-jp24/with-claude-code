from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os
from pathlib import Path

class Settings(BaseSettings):
    # プロジェクト設定
    PROJECT_NAME: str = "アイデア管理SaaS"
    PROJECT_VERSION: str = "0.1.0"
    
    # API設定
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7日間
    
    # データベース設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./idea_management.db")
    
    # CORS設定
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
        "*"  # 開発環境のため一時的に全許可
    ]
    
    # 環境設定
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # LLM API設定
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    CLAUDE_API_KEY: Optional[str] = os.getenv("CLAUDE_API_KEY")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()