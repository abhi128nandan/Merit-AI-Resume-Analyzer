from typing import List

from pydantic import BaseModel, Field

from app.schemas.match_report import MatchReport
from app.schemas.parsed_jd import VerifiedJD
from app.schemas.parsed_resume import VerifiedParsedResume


class AnalysisMetadata(BaseModel):
    analysis_id: str = Field(
        ..., description="Unique Correlation ID (e.g. ANL-20260808-183015-001)"
    )
    generated_at: str = Field(
        ..., description="ISO-8601 Timestamp of report generation"
    )
    processing_time_ms: int = Field(
        ..., description="Total processing time in milliseconds"
    )
    parser_version: str = Field("1.2.0", description="Version of the parsing engine")
    policy_version: str = Field(
        "default-v1", description="Version of the active MatchingPolicy"
    )


class AnalysisFeedback(BaseModel):
    matched_skills: List[str] = Field(
        ..., description="Skills successfully matched from the JD"
    )
    missing_skills: List[str] = Field(
        ..., description="Skills required by the JD but missing from Resume"
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list, description="AI generated suggestions"
    )
    warnings: List[str] = Field(
        default_factory=list, description="Parsing or matching warnings"
    )


class AnalysisResponse(BaseModel):
    metadata: AnalysisMetadata

    # Raw Parsed Data (For Frontend Rendering)
    parsed_resume: VerifiedParsedResume
    parsed_jd: VerifiedJD

    # Evaluated Results
    match_report: MatchReport
    feedback: AnalysisFeedback
