"""
Configuration management for environment variables.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    
    # Security
    bearer_token: str
    
    # Storage
    storage_file: str = "tasks.json"
    
    # Optional
    environment: str = "production"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Cache settings to avoid repeated file reads"""
    return Settings()