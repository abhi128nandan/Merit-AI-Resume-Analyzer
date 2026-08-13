import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from project root directory
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "AI Resume Analyzer"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Database Settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "merit_ai")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./merit_ai.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    BACKEND_CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(",")
    ]


settings = Settings()

if settings.ENVIRONMENT.lower() == "production" and settings.SECRET_KEY == "default_secret_key_change_in_production":
    raise ValueError("SECRET_KEY environment variable MUST be set in production.")
