with open("tests/test_auth.py", "r") as f:
    content = f.read()

# Replace engine config
content = content.replace("from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine", "from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine\nfrom sqlalchemy.pool import StaticPool")
content = content.replace("engine = create_async_engine(TEST_DATABASE_URL, echo=False)", "engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=StaticPool, connect_args={'check_same_thread': False})")

# Append tests
tests = """

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

    # Ensure tables are created in the same StaticPool
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        res = await session.execute(select(User).where(User.email == user_a_email))
        user_a = res.scalars().first()
        report = AnalysisReport(
            user_id=user_a.id,
            resume_filename="user_a_resume.pdf",
            jd_filename="user_a_jd.txt",
            overall_score=92.5,
            full_report_data={"report_content": "top_secret"}
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
"""
content += tests

with open("tests/test_auth.py", "w") as f:
    f.write(content)
