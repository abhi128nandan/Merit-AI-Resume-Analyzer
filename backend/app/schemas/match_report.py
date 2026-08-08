from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class MatchLevel(str, Enum):
    EXACT = "Exact"
    SEMANTIC = "Semantic"
    PARTIAL = "Partial"
    WEAK = "Weak"
    MISSING = "Missing"
    HALLUCINATED = "Hallucinated"


class EvidenceResult(BaseModel):
    requirement: str = Field(..., description="The original requirement from the JD")
    match_level: MatchLevel = Field(..., description="The calculated degree of match")
    evidence_found: str | None = Field(
        None, description="The text from the resume that satisfied this requirement"
    )


class MatchCategoryResult(BaseModel):
    score: int = Field(
        ..., ge=0, le=100, description="Percentage score for this category"
    )
    evidence: List[EvidenceResult] = Field(
        ..., description="The collected evidence justifying the score"
    )


class MatchReport(BaseModel):
    overall_score: int = Field(
        ..., ge=0, le=100, description="Final aggregate ATS match score"
    )

    skills_evaluation: MatchCategoryResult = Field(
        ..., description="Evaluation of required and preferred skills"
    )
    experience_evaluation: MatchCategoryResult = Field(
        ..., description="Evaluation of years of experience"
    )
    education_evaluation: MatchCategoryResult = Field(
        ..., description="Evaluation of degree tiers"
    )
    title_evaluation: MatchCategoryResult = Field(
        ..., description="Evaluation of relevant past job titles"
    )

    confidence_warning: bool = Field(
        ...,
        description="True if underlying parsing had low confidence (e.g. hallucination detected)",
    )
