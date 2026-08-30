from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.core.limiter import limiter

from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from pydantic import BaseModel, EmailStr, Field
from app.core.config import settings
from datetime import datetime, timedelta, timezone

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class Token(BaseModel):
    access_token: str
    token_type: str

import secrets
import hashlib
from app.repositories.postgres.refresh_token_repository import SqlAlchemyRefreshTokenRepository

def _generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def _create_and_set_refresh_token(response: Response, db: AsyncSession, user_id: str):
    token = _generate_refresh_token()
    token_hash = _hash_token(token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    repo = SqlAlchemyRefreshTokenRepository(db)
    await repo.create(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=7 * 24 * 3600
    )

@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Generate token
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=1800
    )
    
    await _create_and_set_refresh_token(response, db, user.id)
    return {"message": "Successfully registered"}

@router.post("/token")
@limiter.limit("5/minute")
async def login(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=1800
    )
    
    await _create_and_set_refresh_token(response, db, user.id)
    return {"message": "Successfully logged in"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.post("/refresh")
async def refresh_token(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
        
    token_hash = _hash_token(refresh_token)
    repo = SqlAlchemyRefreshTokenRepository(db)
    
    token_record = await repo.get_by_hash(token_hash)
    if not token_record or token_record.is_revoked:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    if token_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")
        
    # Get user
    result = await db.execute(select(User).where(User.id == token_record.user_id))
    user = result.scalars().first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
        
    # Rotate token
    await repo.revoke(token_record.id)
    
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=1800
    )
    
    await _create_and_set_refresh_token(response, db, user.id)
    return {"message": "Successfully refreshed token"}

@router.get("/me")
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat()
    }
