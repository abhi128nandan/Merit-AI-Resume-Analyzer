import hashlib
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In production, this must be a secure random string in .env
SECRET_KEY = "merit_ai_super_secret_key_for_local_development"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(pwd_context.hash(password))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)


def sanitize_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)


def generate_unique_filename(original_filename: str) -> str:
    return f"{uuid.uuid4()}_{sanitize_filename(original_filename)}"


def generate_refresh_token() -> str:
    """Generate a secure random string for a refresh token."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash a token using SHA-256 for secure database storage."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
