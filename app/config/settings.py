"""
Application Configuration
"""

# Imports for Pydantic Settings
from pydantic_settings import BaseSettings
from typing import List 


# Imports for Caching and Environment Variables
from functools import lru_cache
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class ApplicationSettings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Settings
    APP_NAME: str = os.getenv("APP_NAME", "Medical Coding API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", True)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = os.getenv("PORT", 8000)

    # CORS
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

@lru_cache
def get_settings() -> ApplicationSettings:
    """Cached settings instance"""
    return ApplicationSettings()

settings = get_settings() # Global settings instance
