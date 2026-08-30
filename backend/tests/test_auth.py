from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_auth.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=StaticPool, connect_args={'check_same_thread': False})
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
    assert "message" in data
    assert response.cookies.get("access_token") is not None
    assert response.cookies.get("refresh_token") is not None

    # Login
    response = client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    # Refresh
    client.cookies.set("refresh_token", refresh_token)
    refresh_response = client.post("/api/v1/auth/refresh")
    assert refresh_response.status_code == 200
    new_data = refresh_response.json()
    assert "message" in new_data
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


import pytest
from sqlalchemy.future import select
from app.models.analysis_report import AnalysisReport
from app.models.user import User

def test_auth_protection_unauthorized_and_valid():
    unauth_client = TestClient(app)
    resp = unauth_client.get("/api/v1/auth/me")
    assert resp.status_code == 401

    user_a_email = "usera_me@example.com"
    user_a_client = TestClient(app)
    reg_a = user_a_client.post(
        "/api/v1/auth/register",
        json={"email": user_a_email, "password": "password123"},
    )
    assert reg_a.status_code == 200
    me_a = user_a_client.get("/api/v1/auth/me")
    assert me_a.status_code == 200
    assert me_a.json()["email"] == user_a_email

@pytest.mark.asyncio
async def test_auth_history_data_isolation_between_users():
    user_a_email = "usera_isolation@example.com"
    user_b_email = "userb_isolation@example.com"

    user_a_client = TestClient(app)
    reg_a = user_a_client.post(
        "/api/v1/auth/register",
        json={"email": user_a_email, "password": "password123"},
    )
    assert reg_a.status_code == 200

    user_b_client = TestClient(app)
    reg_b = user_b_client.post(
        "/api/v1/auth/register",
        json={"email": user_b_email, "password": "password123"},
    )
    assert reg_b.status_code == 200

    me_a = user_a_client.get("/api/v1/auth/me")
    assert me_a.status_code == 200
    user_a_id = me_a.json()["id"]

    # Ensure tables are created in the same StaticPool
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        report = AnalysisReport(
            user_id=user_a_id,
            resume_filename="user_a_resume.pdf",
            jd_filename="user_a_jd.txt",
            overall_score=92.5,
            full_report_data={"report_content": "top_secret"},
            is_deleted=False
        )
        session.add(report)
        await session.commit()
        await session.refresh(report)
        report_id = report.id

    resp_a = user_a_client.get(f"/api/v1/history/{report_id}")
    assert resp_a.status_code == 200
    assert resp_a.json() == {"report_content": "top_secret"}

    resp_b = user_b_client.get(f"/api/v1/history/{report_id}")
    assert resp_b.status_code == 404
