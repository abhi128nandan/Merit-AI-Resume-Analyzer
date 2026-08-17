from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    """Response schema returned after a successful resume file upload."""

    file_id: str = Field(
        ...,
        description="Unique UUID identifier for the uploaded file.",
    )
    original_filename: str = Field(
        ...,
        description="Sanitized original filename from the client.",
    )
    stored_filename: str = Field(
        ...,
        description="UUID-based filename stored on disk.",
    )
    file_size: int = Field(
        ...,
        ge=0,
        description="Size of the uploaded file in bytes.",
    )
    content_type: str = Field(
        ...,
        description="MIME content type of the uploaded file.",
    )
    status: str = Field(
        default="uploaded",
        description="Current processing status of the resume.",
    )
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of when the file was uploaded.",
    )
