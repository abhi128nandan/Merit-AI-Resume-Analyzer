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


def test_register_and_login():
    email = "testauth@example.com"
    password = "securepassword"

    # Register
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None

    # Login
    response = client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    # Refresh
    client.cookies.set("refresh_token", refresh_token)
    refresh_response = client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 200
    new_data = refresh_response.json()
    assert "access_token" in new_data
    new_refresh_token = refresh_response.cookies.get("refresh_token")
    assert new_refresh_token is not None
    assert refresh_token != new_refresh_token  # Token should rotate

    # Logout
    logout_response = client.post("/api/v1/auth/logout")
    assert logout_response.status_code == 200
    # TestClient deleting cookies sometimes sets them to empty or removes them
    assert (
        "access_token" not in logout_response.cookies
        or not logout_response.cookies.get("access_token")
    )
