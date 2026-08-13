from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.repositories.interfaces.user_repository import IUserRepository


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_password(self, user_id: str, new_hashed_password: str) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        setattr(user, "hashed_password", new_hashed_password)
        await self.db.commit()
        await self.db.refresh(user)
        return True
