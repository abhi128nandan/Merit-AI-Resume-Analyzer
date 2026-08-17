import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Use SQLite for local development by default, or Postgres if DATABASE_URL is set in prod/docker.
DEFAULT_DB_URL = "sqlite+aiosqlite:///./merit_ai.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    """FastAPI Dependency for database sessions."""
    async with SessionLocal() as session:
        yield session
