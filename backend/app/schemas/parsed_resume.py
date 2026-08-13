from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class LLMExtractedExperience(BaseModel):
    title: str = Field("Software Engineer", description="Job title")
    company: str = Field("Not Specified", description="Company name")
    start_date: str = Field("", description="Start date (e.g., 'Jan 2020')")
    end_date: str = Field("", description="End date (e.g., 'Present' or 'Dec 2022')")
    responsibilities: List[str] = Field(
        default_factory=list,
        description="List of bullet points describing responsibilities and achievements",
    )

    @field_validator("title", "company", "start_date", "end_date", mode="before")
    @classmethod
    def sanitize_strings(cls, v: Optional[str]) -> str:
        return "" if v is None else str(v).strip()

    @field_validator("responsibilities", mode="before")
    @classmethod
    def sanitize_responsibilities(cls, v: Optional[List[str]]) -> List[str]:
        return [] if v is None else [str(x) for x in v if x is not None]


class LLMExtractedEducation(BaseModel):
    degree: str = Field(
        "Degree", description="Degree obtained (e.g., 'B.S. Computer Science')"
    )
    institution: str = Field("Not Specified", description="University or college name")
    graduation_year: str = Field("", description="Year of graduation (e.g., '2021')")
    coursework: List[str] = Field(
        default_factory=list, description="List of relevant coursework or subjects studied"
    )

    @field_validator("degree", "institution", "graduation_year", mode="before")
    @classmethod
    def sanitize_strings(cls, v: Optional[str]) -> str:
        return "" if v is None else str(v).strip()

    @field_validator("coursework", mode="before")
    @classmethod
    def sanitize_coursework(cls, v: Optional[List[str]]) -> List[str]:
        return [] if v is None else [str(x) for x in v if x is not None]


class LLMExtractedContact(BaseModel):
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")


class LLMExtractedResume(BaseModel):
    """The raw JSON structure expected from the LLM extraction step."""

    contact: LLMExtractedContact = Field(
        default_factory=lambda: LLMExtractedContact(
            email=None, phone=None, linkedin=None
        )
    )
    summary: Optional[str] = Field(
        None, description="Professional summary or objective"
    )
    skills: List[str] = Field(
        default_factory=list, description="List of all skills extracted (hard and soft)"
    )
    experience: List[LLMExtractedExperience] = Field(default_factory=list)
    education: List[LLMExtractedEducation] = Field(default_factory=list)

    @field_validator("skills", "experience", "education", mode="before")
    @classmethod
    def sanitize_lists(cls, v: Optional[List]) -> List:
        return [] if v is None else v


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
    coursework: List[VerifiedField]


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
