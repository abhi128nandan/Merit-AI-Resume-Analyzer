from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_history_unauthorized():
    response = client.get("/api/v1/history/")
    assert response.status_code == 401


def test_history_flow():
    email = "history_tester@example.com"
    password = "securepassword"

    # Register to get an authenticated user
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    
    # The client automatically handles cookies returned by registration/login
    
    # 1. Test empty history with pagination structure
    response = client.get("/api/v1/history/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    
    # 2. Test deleting a non-existent report
    response = client.delete("/api/v1/history/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
