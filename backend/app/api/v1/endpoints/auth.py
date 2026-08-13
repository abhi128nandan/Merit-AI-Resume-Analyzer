from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    get_password_hash,
    hash_token,
    verify_password,
)
from app.models.user import User
from app.repositories.postgres.refresh_token_repository import (
    SqlAlchemyRefreshTokenRepository,
)

router = APIRouter()


async def _set_tokens(response: Response, db: AsyncSession, user: User) -> dict:
    access_token = create_access_token(data={"sub": user.email})
    refresh_token_value = generate_refresh_token()

    refresh_repo = SqlAlchemyRefreshTokenRepository(db)
    expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=7)
    await refresh_repo.create(
        user_id=str(user.id),
        token_hash=hash_token(refresh_token_value),
        expires_at=expires_at,
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=1800,  # 30 mins
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token_value,
        httponly=True,
        samesite="lax",
        secure=(settings.ENVIRONMENT == "production"),
        max_age=7 * 24 * 60 * 60,
        path="/api/v1/auth/refresh",
    )
    return {"access_token": access_token, "token_type": "bearer"}


class UserCreate(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=Token)
async def register(
    user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(
        email=user_in.email, hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return await _set_tokens(response, db, user)


@router.post("/token", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _set_tokens(response, db, user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    token_value = request.cookies.get("refresh_token")
    if not token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    refresh_repo = SqlAlchemyRefreshTokenRepository(db)
    stored_token = await refresh_repo.get_by_hash(hash_token(token_value))

    if (
        not stored_token
        or stored_token.is_revoked
        or stored_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None)
    ):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token", path="/api/v1/auth/refresh")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Valid token found. Revoke it for rotation.
    await refresh_repo.revoke(str(stored_token.id))

    # Get user
    result = await db.execute(select(User).where(User.id == stored_token.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return await _set_tokens(response, db, user)


@router.post("/logout")
async def logout(
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    refresh_repo = SqlAlchemyRefreshTokenRepository(db)
    await refresh_repo.revoke_all_user_tokens(str(current_user.id))

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/api/v1/auth/refresh")
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }
