import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # API Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Environment
    ENV: str = os.getenv("ENV", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Ensure critical settings are set in production
if settings.ENV == "production":
    assert settings.SECRET_KEY != "development-key-change-in-production", \
        "Production SECRET_KEY must be set"
    assert not settings.DATABASE_URL.startswith("sqlite"), \
        "Production must use PostgreSQL, not SQLite"