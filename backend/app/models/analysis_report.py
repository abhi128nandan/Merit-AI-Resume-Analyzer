import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(
        String().with_variant(UUID(as_uuid=True), "postgresql"),
        primary_key=True,
        default=generate_uuid,
        index=True,
    )
    user_id = Column(
        String().with_variant(UUID(as_uuid=True), "postgresql"),
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    resume_filename = Column(String, nullable=False)
    jd_filename = Column(String, nullable=False)
    overall_score = Column(Float, nullable=False)

    # The complete JSON response payload stored as a JSON object.
    # This allows the frontend dashboard to re-hydrate the exact report state.
    full_report_data = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False)

    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    user = relationship("User", back_populates="analysis_reports")
