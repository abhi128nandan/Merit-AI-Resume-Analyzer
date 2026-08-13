from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base
from app.repositories.postgres.refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)
from app.repositories.postgres.user_repository import SqlAlchemyUserRepository

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_user_repository_crud(db_session: AsyncSession):
    user_repo = SqlAlchemyUserRepository(db_session)

    # Create user
    user = await user_repo.create("test_repo@example.com", "hashed_pass_123")
    assert user.id is not None
    assert user.email == "test_repo@example.com"

    # Get by email
    fetched_by_email = await user_repo.get_by_email("test_repo@example.com")
    assert fetched_by_email is not None
    assert fetched_by_email.id == user.id

    # Get by ID
    fetched_by_id = await user_repo.get_by_id(str(user.id))
    assert fetched_by_id is not None
    assert fetched_by_id.email == "test_repo@example.com"

    # Update password
    updated = await user_repo.update_password(str(user.id), "new_hashed_pass_456")
    assert updated is True
    refreshed_user = await user_repo.get_by_id(str(user.id))
    assert refreshed_user is not None
    assert refreshed_user.hashed_password == "new_hashed_pass_456"


@pytest.mark.asyncio
async def test_refresh_token_repository_operations(db_session: AsyncSession):
    user_repo = SqlAlchemyUserRepository(db_session)
    token_repo = SqlAlchemyRefreshTokenRepository(db_session)

    # Create parent user
    user = await user_repo.create("token_repo@example.com", "hashed_pass")

    # Create token
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    token_hash = "sample_sha256_hash_value_123"
    token = await token_repo.create(str(user.id), token_hash, expires_at)
    assert token.id is not None
    assert token.user_id == user.id
    assert token.is_revoked is False

    # Fetch by hash
    fetched = await token_repo.get_by_hash(token_hash)
    assert fetched is not None
    assert fetched.id == token.id

    # Revoke single token
    revoked = await token_repo.revoke(token.id)
    assert revoked is True
    refreshed_token = await token_repo.get_by_hash(token_hash)
    assert refreshed_token is not None
    assert refreshed_token.is_revoked is True

    # Create second token & test bulk revocation
    token2_hash = "sample_sha256_hash_value_456"
    token2 = await token_repo.create(user.id, token2_hash, expires_at)
    assert token2.is_revoked is False

    count = await token_repo.revoke_all_user_tokens(user.id)
    assert count >= 1
    refreshed_token2 = await token_repo.get_by_hash(token2_hash)
    assert refreshed_token2 is not None
    assert refreshed_token2.is_revoked is True
