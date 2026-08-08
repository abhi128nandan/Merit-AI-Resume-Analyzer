import re

from app.core.logging import logger
from app.exceptions.custom_exceptions import NotAJobDescriptionException


def is_valid_jd(text: str) -> bool:
    """Deterministically detects if the provided text is likely a job description.

    Scores the text based on common JD indicators:
    - Keywords like 'requirements', 'qualifications', 'responsibilities'
    - Mentions of 'experience', 'years'
    - Employment types (full-time, part-time)

    If the score is less than 3, it is deemed NOT a JD.

    Args:
        text: The cleaned, normalized text string.

    Returns:
        True if the text is a valid JD, False otherwise.

    Raises:
        NotAJobDescriptionException: If the score is below the threshold.
    """
    score = 0
    text_lower = text.lower()

    # 1. Core JD Sections
    core_sections = [
        "requirements",
        "qualifications",
        "responsibilities",
        "what you'll do",
        "what you will do",
        "duties",
        "nice to have",
        "preferred",
    ]
    sections_found = sum(
        1 for sec in core_sections if re.search(rf"\b{sec}\b", text_lower)
    )
    score += min(sections_found, 3)  # Cap at 3 points

    # 2. Experience indicators
    if re.search(
        r"\b\d+\+?\s*(?:-\s*\d+\s*)?years?(?:\s+[\w-]+){0,3}\s+experience\b",
        text_lower,
    ):
        score += 2

    # 3. Employment type indicators
    employment_types = [
        "full-time",
        "full time",
        "part-time",
        "part time",
        "contract",
        "remote",
        "hybrid",
    ]
    if any(re.search(rf"\b{et}\b", text_lower) for et in employment_types):
        score += 1

    logger.info(f"JD Detection Score: {score}/6")

    # Threshold for validity is 3.
    if score < 3:
        raise NotAJobDescriptionException(
            details={
                "score": score,
                "threshold": 3,
                "message": "Missing key Job Description indicators (requirements, experience).",
            }
        )

    return True
