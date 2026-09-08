from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "KalaConnect-AI Backend"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    AI_MODE: str = "mock"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # API Keys
    LLM_API_KEY: str | None = None
    VISION_API_KEY: str | None = None
    SPEECH_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
