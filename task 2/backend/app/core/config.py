from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./medipredict.db"
    ai_provider: str = "openai"
    ai_api_key: Optional[str] = None
    ai_model: str = "gpt-3.5-turbo"
    ai_base_url: str = "https://api.openai.com/v1"
    ai_timeout_seconds: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
