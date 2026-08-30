import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from dotenv import load_dotenv

# Load .env file from project root directory
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


    model_config = SettingsConfigDict(
        env_file=str(env_path),
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_secret_key(self) -> 'Settings':
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == "default_secret_key_change_in_production":
            raise ValueError("SECRET_KEY must be set in production")
        return self

settings = Settings()
