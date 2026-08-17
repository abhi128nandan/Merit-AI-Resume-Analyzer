from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class LLMExtractedJD(BaseModel):
    """The raw JSON structure expected from the LLM extraction step for Job Descriptions."""

    job_title: str = Field(
        "Job Title Not Specified", description="The official job title"
    )
    company: str = Field("Not Specified", description="The hiring company name")
    location: str = Field(
        "Not Specified", description="Location of the job (e.g. Remote, New York, NY)"
    )
    employment_type: str = Field(
        "Full-time", description="e.g. Full-time, Contract, Part-time"
    )
    required_skills: List[str] = Field(
        default_factory=list,
        description="Skills explicitly stated as required or mandatory",
    )
    preferred_skills: List[str] = Field(
        default_factory=list,
        description="Skills stated as preferred, nice-to-have, or a plus",
    )
    responsibilities: List[str] = Field(
        default_factory=list, description="Day-to-day responsibilities and duties"
    )
    qualifications: List[str] = Field(
        default_factory=list, description="General qualifications and certifications"
    )
    experience_requirements: str = Field(
        "Not Specified", description="Experience range requested (e.g. 3-5 years)"
    )
    education_requirements: str = Field(
        "Not Specified",
        description="Educational requirements (e.g. Bachelor's Degree in CS)",
    )

    @field_validator(
        "job_title",
        "company",
        "location",
        "employment_type",
        "experience_requirements",
        "education_requirements",
        mode="before",
    )
    @classmethod
    def sanitize_null_strings(cls, v: Optional[str]) -> str:
        if v is None or not str(v).strip():
            return "Not Specified"
        return str(v).strip()

    @field_validator(
        "required_skills",
        "preferred_skills",
        "responsibilities",
        "qualifications",
        mode="before",
    )
    @classmethod
    def sanitize_null_lists(cls, v: Optional[List[str]]) -> List[str]:
        if v is None:
            return []
        return [str(item) for item in v if item is not None]


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
