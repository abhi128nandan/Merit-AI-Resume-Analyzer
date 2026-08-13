from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.models.refresh_token import RefreshToken


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def create(
        self, user_id: str, token_hash: str, expires_at: datetime
    ) -> RefreshToken:
        """Create and persist a new RefreshToken entity."""

    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Retrieve a RefreshToken by its SHA-256 hash."""

    @abstractmethod
    async def revoke(self, token_id: str) -> bool:
        """Mark a specific refresh token as revoked."""

    @abstractmethod
    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all active refresh tokens for a user (security reuse breach response)."""
