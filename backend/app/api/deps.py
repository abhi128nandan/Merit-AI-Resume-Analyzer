from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import ALGORITHM
from app.models.user import User

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token")
    if not token or not token.startswith("Bearer "):
        raise credentials_exception
        
    token = token[len("Bearer "):]
    
    try:
        from app.core.config import settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user


from typing import Optional

async def get_optional_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> Optional[User]:
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None
