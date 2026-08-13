from datetime import datetime
from typing import Optional

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.refresh_token import RefreshToken
from app.repositories.interfaces.refresh_token_repository import IRefreshTokenRepository


class SqlAlchemyRefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, user_id: str, token_hash: str, expires_at: datetime
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            is_revoked=False,
        )
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalars().first()

    async def revoke(self, token_id: str) -> bool:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.id == token_id)
        )
        token = result.scalars().first()
        if not token:
            return False
        setattr(token, "is_revoked", True)
        await self.db.commit()
        return True

    async def revoke_all_user_tokens(self, user_id: str) -> int:
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked.is_(False))
            .values(is_revoked=True)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return int(getattr(result, "rowcount", 0))
