from typing import List, Optional

from pydantic import BaseModel, Field


class LLMExtractedExperience(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    start_date: str = Field(..., description="Start date (e.g., 'Jan 2020')")
    end_date: str = Field(..., description="End date (e.g., 'Present' or 'Dec 2022')")
    responsibilities: List[str] = Field(
        ...,
        description="List of bullet points describing responsibilities and achievements",
    )


class LLMExtractedEducation(BaseModel):
    degree: str = Field(
        ..., description="Degree obtained (e.g., 'B.S. Computer Science')"
    )
    institution: str = Field(..., description="University or college name")
    graduation_year: str = Field(..., description="Year of graduation (e.g., '2021')")


class LLMExtractedContact(BaseModel):
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")


class LLMExtractedResume(BaseModel):
    """The raw JSON structure expected from the LLM extraction step."""

    contact: LLMExtractedContact
    summary: Optional[str] = Field(
        None, description="Professional summary or objective"
    )
    skills: List[str] = Field(
        ..., description="List of all skills extracted (hard and soft)"
    )
    experience: List[LLMExtractedExperience]
    education: List[LLMExtractedEducation]


class VerifiedField(BaseModel):
    """A wrapper for a field that has been cross-checked against the original text."""

    value: str
    verification_state: str = Field(
        ...,
        description="One of: 'Verified', 'Partially Verified', 'Unverified', 'Hallucinated'",
    )


class VerifiedExperience(BaseModel):
    title: VerifiedField
    company: VerifiedField
    start_date: VerifiedField
    end_date: VerifiedField
    responsibilities: List[VerifiedField]


class VerifiedEducation(BaseModel):
    degree: VerifiedField
    institution: VerifiedField
    graduation_year: VerifiedField


class VerifiedContact(BaseModel):
    email: Optional[VerifiedField]
    phone: Optional[VerifiedField]
    linkedin: Optional[VerifiedField]


class VerifiedParsedResume(BaseModel):
    """The final enriched structure after deterministic hallucination verification."""

    contact: VerifiedContact
    summary: Optional[VerifiedField]
    skills: List[VerifiedField]
    experience: List[VerifiedExperience]
    education: List[VerifiedEducation]

    # Confidence metrics
    overall_confidence: int = Field(..., ge=0, le=100)
    section_confidence: dict[str, int] = Field(
        ..., description="Confidence scores per section"
    )
