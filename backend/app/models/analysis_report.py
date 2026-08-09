import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    
    resume_filename = Column(String, nullable=False)
    jd_filename = Column(String, nullable=False)
    overall_score = Column(Float, nullable=False)
    
    # The complete JSON response payload stored as a JSON object.
    # This allows the frontend dashboard to re-hydrate the exact report state.
    full_report_data = Column(JSON, nullable=False)
    
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="analysis_reports")
