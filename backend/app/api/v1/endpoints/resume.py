from fastapi import APIRouter, File, UploadFile

from app.schemas.resume import ResumeUploadResponse
from app.services.upload_service import save_uploaded_file

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    status_code=200,
    summary="Upload a resume file",
    description=(
        "Accepts a PDF or DOCX resume file via multipart form upload. "
        "Validates file type, size, and extension, then stores it "
        "securely with a UUID-based filename."
    ),
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
) -> ResumeUploadResponse:
    """Upload and validate a resume file."""
    return await save_uploaded_file(file)
