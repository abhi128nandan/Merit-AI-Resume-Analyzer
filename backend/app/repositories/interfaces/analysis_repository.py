from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.analysis_report import AnalysisReport


class IAnalysisRepository(ABC):
    @abstractmethod
    async def get_history(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[AnalysisReport]:
        """Retrieve a paginated list of active analysis reports for a user."""

    @abstractmethod
    async def save_report(self, report: AnalysisReport) -> None:
        """Persist a new analysis report."""

    @abstractmethod
    async def get_report(
        self, user_id: str, analysis_id: str
    ) -> Optional[AnalysisReport]:
        """Retrieve a specific analysis report by ID, validating ownership."""

    @abstractmethod
    async def delete_report(self, user_id: str, analysis_id: str) -> bool:
        """Soft-delete an analysis report. Returns True if deleted, False if not found."""

    @abstractmethod
    async def count_reports(self, user_id: str) -> int:
        """Count the total number of active analysis reports for a user."""
