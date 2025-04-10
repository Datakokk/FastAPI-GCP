from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application configuration"""
    APP_TITLE: str = "Firebase Authentication API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for Firebase Authentication"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True

    # Cors
    CORS_ALLOWED_ORIGINS: List[str] = []
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: Optional[str] = "firebase-credentials.json"
    FIREBASE_CREDENTIALS_JSON: Optional[str] = None
    

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


settings = Settings()

