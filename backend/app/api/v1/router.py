from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.exceptions.custom_exceptions import ResumeAnalyzerException
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import execute_analysis_workflow
from app.validators.file_validator import validate_uploaded_file
from app.api.v1.endpoints import auth, history
from app.core.database import get_db
from app.api.deps import get_optional_current_user
from app.models.user import User
from app.models.analysis_report import AnalysisReport
import json

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(history.router, prefix="/history", tags=["history"])

@api_v1_router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Analyze a Resume against a Job Description",
    description="Uploads a resume (PDF/DOCX) and job description (PDF/DOCX/TXT), orchestrates the AI parsing pipelines concurrently, runs the ATS matching engine, and returns a comprehensive structured report.",
    status_code=200,
)
async def analyze_documents(
    resume: UploadFile = File(..., description="The candidate's resume (PDF/DOCX)"),
    jd: UploadFile = File(..., description="The target Job Description (PDF/DOCX/TXT)"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> AnalysisResponse:
    """The main entry point for the AI Resume Analyzer V1."""

    resume_filename = resume.filename or ""
    jd_filename = jd.filename or ""
    resume_content_type = resume.content_type or ""
    jd_content_type = jd.content_type or ""

    logger.info(
        f"Received /analyze request. Resume: {resume_filename}, JD: {jd_filename}"
    )

    # 1. Validation (Synchronous bounds check before doing heavy lifting)
    try:
        # We read the bytes into memory. Since FileTooLargeException guards size, this is safe.
        resume_bytes = await resume.read()
        jd_bytes = await jd.read()

        # Validate magic bytes / structure
        validate_uploaded_file(
            filename=resume_filename,
            content_type=resume_content_type,
            file_size=len(resume_bytes),
            file_content=resume_bytes,
        )
        validate_uploaded_file(
            filename=jd_filename,
            content_type=jd_content_type,
            file_size=len(jd_bytes),
            file_content=jd_bytes,
        )

    except ResumeAnalyzerException as e:
        # Expected domain validations (e.g. InvalidFileUploadException, UnsupportedFileTypeException)
        logger.warning(f"File validation failed: {e.message}")
        raise e  # Let global exception handler catch this and map to 422/415
    except Exception as e:
        logger.error(f"Unexpected error during file read/validation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process uploaded files.")

    # 2. Orchestration (Delegated to AnalysisService)
    # The router does NO business logic. It waits for the service.
    try:
        response = await execute_analysis_workflow(
            resume_bytes=resume_bytes,
            resume_filename=resume_filename,
            jd_bytes=jd_bytes,
            jd_filename=jd_filename,
        )
        
        # Save to database if authenticated
        if current_user:
            report_record = AnalysisReport(
                user_id=current_user.id,
                resume_filename=resume_filename,
                jd_filename=jd_filename,
                overall_score=response.match_report.overall_score,
                full_report_data=response.model_dump()
            )
            db.add(report_record)
            await db.commit()
            
        return response
    except ResumeAnalyzerException as e:
        # Passes the error up to the global handler
        raise e
    except Exception as e:
        logger.critical(f"Analysis Workflow failed completely: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error during analysis."
        )
