from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.interfaces.analysis_repository import IAnalysisRepository
from app.repositories.postgres.analysis_repository import SqlAlchemyAnalysisRepository

router = APIRouter()


def get_analysis_repository(db: AsyncSession = Depends(get_db)) -> IAnalysisRepository:
    return SqlAlchemyAnalysisRepository(db)


@router.get("/", response_model=Dict[str, Any])
async def get_history(
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(10, ge=1, le=100, description="Return up to N records"),
    repo: IAnalysisRepository = Depends(get_analysis_repository),
    current_user: User = Depends(get_current_user),
):
    """Fetches a paginated list of past analysis reports for the authenticated user."""
    reports = await repo.get_history(user_id=str(current_user.id), skip=skip, limit=limit)
    total_count = await repo.count_reports(user_id=str(current_user.id))

    # Return a paginated structure with summary list
    return {
        "items": [
            {
                "id": r.id,
                "resume_filename": r.resume_filename,
                "jd_filename": r.jd_filename,
                "overall_score": r.overall_score,
                "created_at": r.created_at.isoformat(),
            }
            for r in reports
        ],
        "total": total_count,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "size": limit,
    }


@router.get("/{analysis_id}", response_model=dict)
async def get_analysis(
    analysis_id: str,
    repo: IAnalysisRepository = Depends(get_analysis_repository),
    current_user: User = Depends(get_current_user),
):
    """Fetches a specific full analysis report by ID."""
    report = await repo.get_report(user_id=str(current_user.id), analysis_id=analysis_id)

    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")

    return report.full_report_data


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    repo: IAnalysisRepository = Depends(get_analysis_repository),
    current_user: User = Depends(get_current_user),
):
    """Soft deletes a specific analysis report by ID."""
    deleted = await repo.delete_report(user_id=str(current_user.id), analysis_id=analysis_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis report not found")

    return {"message": "Analysis report deleted successfully"}
