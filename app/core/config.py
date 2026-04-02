import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Dashboard Backend"
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "finance_db"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_HERE"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Allow extra environment variables without throwing an error
        extra="ignore"
    )

settings = Settings()
