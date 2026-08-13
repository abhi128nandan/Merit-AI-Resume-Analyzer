from abc import ABC, abstractmethod
from typing import Optional

from app.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their primary key ID."""

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""

    @abstractmethod
    async def create(self, email: str, hashed_password: str) -> User:
        """Create and persist a new User entity."""

    @abstractmethod
    async def update_password(self, user_id: str, new_hashed_password: str) -> bool:
        """Update a user's hashed password."""
