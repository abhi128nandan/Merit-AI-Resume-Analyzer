from pydantic import BaseModel, Field


class MatchingPolicy(BaseModel):
    """Configurable weights for the ATS Scoring Engine."""

    # Category Weights (Must sum to 1.0 or 100)
    skills_weight: float = Field(default=0.40, description="Weight for skills matching")
    experience_weight: float = Field(
        default=0.30, description="Weight for experience matching"
    )
    education_weight: float = Field(
        default=0.15, description="Weight for education matching"
    )
    title_weight: float = Field(
        default=0.15, description="Weight for job title matching"
    )

    # Sub-weights for Skills
    required_skills_weight: float = Field(
        default=0.75, description="Importance of required skills vs preferred"
    )
    preferred_skills_weight: float = Field(
        default=0.25, description="Importance of preferred skills vs required"
    )

    # Match Level scoring multipliers
    score_exact: float = Field(default=1.0, description="Multiplier for Exact match")
    score_semantic: float = Field(
        default=0.9, description="Multiplier for Semantic match"
    )
    score_partial: float = Field(
        default=0.5, description="Multiplier for Partial match"
    )
    score_weak: float = Field(default=0.2, description="Multiplier for Weak match")
    score_missing: float = Field(
        default=0.0, description="Multiplier for Missing match"
    )
    score_hallucinated: float = Field(
        default=0.0, description="Multiplier for Hallucinated match"
    )

    def validate_weights(self) -> None:
        """Ensures weights sum up to 1.0 (with slight float tolerance)."""
        total = (
            self.skills_weight
            + self.experience_weight
            + self.education_weight
            + self.title_weight
        )
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Category weights must sum to 1.0. Current sum: {total}")

        skills_total = self.required_skills_weight + self.preferred_skills_weight
        if abs(skills_total - 1.0) > 0.001:
            raise ValueError(
                f"Skills sub-weights must sum to 1.0. Current sum: {skills_total}"
            )


# Default Policy
DEFAULT_POLICY = MatchingPolicy()
