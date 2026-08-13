import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(
        String().with_variant(UUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=generate_uuid,
        index=True,
    )
    user_id = Column(
        String().with_variant(UUID(as_uuid=True), "postgresql"),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    token_hash = Column(String, unique=True, index=True, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False
    )

    user = relationship("User", back_populates="refresh_tokens")
