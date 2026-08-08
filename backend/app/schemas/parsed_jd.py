from typing import List

from pydantic import BaseModel, Field


class LLMExtractedJD(BaseModel):
    """The raw JSON structure expected from the LLM extraction step for Job Descriptions."""

    job_title: str = Field(..., description="The official job title")
    company: str = Field(..., description="The hiring company name")
    location: str = Field(
        ..., description="Location of the job (e.g. Remote, New York, NY)"
    )
    employment_type: str = Field(..., description="e.g. Full-time, Contract, Part-time")
    required_skills: List[str] = Field(
        ..., description="Skills explicitly stated as required or mandatory"
    )
    preferred_skills: List[str] = Field(
        ..., description="Skills stated as preferred, nice-to-have, or a plus"
    )
    responsibilities: List[str] = Field(
        ..., description="Day-to-day responsibilities and duties"
    )
    qualifications: List[str] = Field(
        ..., description="General qualifications and certifications"
    )
    experience_requirements: str = Field(
        ..., description="Experience range requested (e.g. 3-5 years)"
    )
    education_requirements: str = Field(
        ..., description="Educational requirements (e.g. Bachelor's Degree in CS)"
    )


class VerifiedJDField(BaseModel):
    """A wrapper for a field that has been cross-checked against the original text."""

    value: str
    verification_state: str = Field(
        ...,
        description="One of: 'Verified', 'Partially Verified', 'Unverified', 'Hallucinated'",
    )


class VerifiedJD(BaseModel):
    """The final enriched structure after deterministic hallucination verification for JD."""

    job_title: VerifiedJDField
    company: VerifiedJDField
    location: VerifiedJDField
    employment_type: VerifiedJDField
    required_skills: List[VerifiedJDField]
    preferred_skills: List[VerifiedJDField]
    responsibilities: List[VerifiedJDField]
    qualifications: List[VerifiedJDField]
    experience_requirements: VerifiedJDField
    education_requirements: VerifiedJDField

    # Confidence metrics
    overall_confidence: int = Field(..., ge=0, le=100)
    section_confidence: dict[str, int] = Field(
        ..., description="Confidence scores per section"
    )
