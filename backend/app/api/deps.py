from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import ALGORITHM
from app.models.user import User

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    # Authentication bypassed
    email = "admin@merit.ai"
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        user = User(
            email=email,
            hashed_password="bypassed_no_password",
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    return user


from typing import Optional

async def get_optional_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> Optional[User]:
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None
