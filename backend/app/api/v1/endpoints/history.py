from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Any
import json

from app.core.database import get_db
from app.models.analysis_report import AnalysisReport
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches all past analysis reports for the authenticated user."""
    result = await db.execute(
        select(AnalysisReport)
        .where(AnalysisReport.user_id == current_user.id)
        .where(AnalysisReport.is_deleted == False)
        .order_by(AnalysisReport.created_at.desc())
    )
    reports = result.scalars().all()
    
    # Return a summary list (not the full JSON blob which is heavy)
    return [
        {
            "id": r.id,
            "resume_filename": r.resume_filename,
            "jd_filename": r.jd_filename,
            "overall_score": r.overall_score,
            "created_at": r.created_at.isoformat()
        }
        for r in reports
    ]


@router.get("/{analysis_id}", response_model=dict)
async def get_analysis(analysis_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches a specific full analysis report by ID."""
    result = await db.execute(
        select(AnalysisReport)
        .where(AnalysisReport.id == analysis_id)
        .where(AnalysisReport.user_id == current_user.id)
        .where(AnalysisReport.is_deleted == False)
    )
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")
        
    return report.full_report_data

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(analysis_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Soft-deletes a specific analysis report by ID."""
    result = await db.execute(
        select(AnalysisReport)
        .where(AnalysisReport.id == analysis_id)
        .where(AnalysisReport.user_id == current_user.id)
        .where(AnalysisReport.is_deleted == False)
    )
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Analysis report not found")
        
    report.is_deleted = True
    await db.commit()
    return None

