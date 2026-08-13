from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update

from app.models.analysis_report import AnalysisReport
from app.repositories.interfaces.analysis_repository import IAnalysisRepository


class SqlAlchemyAnalysisRepository(IAnalysisRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_history(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[AnalysisReport]:
        result = await self.db.execute(
            select(AnalysisReport)
            .where(AnalysisReport.user_id == user_id)
            .where(AnalysisReport.is_deleted.is_(False))
            .order_by(AnalysisReport.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def save_report(self, report: AnalysisReport) -> None:
        self.db.add(report)
        await self.db.commit()

    async def get_report(
        self, user_id: str, analysis_id: str
    ) -> Optional[AnalysisReport]:
        result = await self.db.execute(
            select(AnalysisReport)
            .where(AnalysisReport.id == analysis_id)
            .where(AnalysisReport.user_id == user_id)
            .where(AnalysisReport.is_deleted.is_(False))
        )
        return result.scalars().first()

    async def delete_report(self, user_id: str, analysis_id: str) -> bool:
        # First verify it exists and is not already deleted
        report = await self.get_report(user_id, analysis_id)
        if not report:
            return False

        await self.db.execute(
            update(AnalysisReport)
            .where(AnalysisReport.id == analysis_id)
            .where(AnalysisReport.user_id == user_id)
            .values(is_deleted=True)
        )
        await self.db.commit()
        return True

    async def count_reports(self, user_id: str) -> int:
        result = await self.db.execute(
            select(func.count(AnalysisReport.id))
            .where(AnalysisReport.user_id == user_id)
            .where(AnalysisReport.is_deleted.is_(False))
        )
        count = result.scalar()
        return count if count is not None else 0
