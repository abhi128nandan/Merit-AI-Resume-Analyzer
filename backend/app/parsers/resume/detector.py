import re

from app.core.logging import logger
from app.exceptions.custom_exceptions import NotAResumeException


def is_valid_resume(text: str) -> bool:
    """Deterministically detects if the provided text is likely a resume.

    Scores the text based on common resume indicators:
    - Email address (1 point)
    - Phone number (1 point)
    - LinkedIn URL (1 point)
    - Standard section headers (1 point each, max 3)

    If the score is less than 3, it is deemed NOT a resume.

    Args:
        text: The cleaned, normalized text string.

    Returns:
        True if the text is a valid resume, False otherwise.

    Raises:
        NotAResumeException: If the score is below the threshold.
    """
    score = 0

    # 1. Email Regex
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    if re.search(email_pattern, text):
        score += 1

    # 2. Phone Regex (various formats)
    phone_pattern = r"(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    if re.search(phone_pattern, text):
        score += 1

    # 3. LinkedIn URL
    if "linkedin.com/in/" in text.lower():
        score += 1

    # 4. Section Headers (case insensitive, usually preceded/followed by newlines)
    # We look for common keywords
    text_lower = text.lower()
    sections_found = 0
    common_sections = [
        "experience",
        "education",
        "skills",
        "projects",
        "summary",
        "objective",
        "certifications",
    ]

    for section in common_sections:
        # Match whole words to avoid false positives (e.g. "experiencing")
        if re.search(rf"\b{section}\b", text_lower):
            sections_found += 1
            if sections_found >= 3:
                break

    score += min(sections_found, 3)

    logger.info(f"Resume Detection Score: {score}/6")

    # Threshold for validity is 3.
    # Examples of valid combos: (Email + Phone + Experience), or (3 Sections), etc.
    if score < 3:
        raise NotAResumeException(
            details={
                "score": score,
                "threshold": 3,
                "message": "Missing key resume indicators (email, phone, standard sections).",
            }
        )

    return True
