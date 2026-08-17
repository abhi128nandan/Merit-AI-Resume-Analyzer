import pytest

from app.exceptions.custom_exceptions import NotAResumeException
from app.parsers.resume.cleaner import clean_extracted_text
from app.parsers.resume.detector import is_valid_resume
from app.parsers.resume.verifier import verify_field


def test_text_cleaner():
    """Tests deterministic text normalization rules."""
    raw_text = "This  is\t\t a   test.\r\n\r\n\r\nNext line. • Bullet 1 \u2022 Bullet 2"
    cleaned = clean_extracted_text(raw_text)

    # 1. Multiple spaces should be collapsed per line
    # 2. \r\n should be \n
    # 3. Bullets should be converted to '-'

    assert "This is a test." in cleaned
    assert "Next line. - Bullet 1 - Bullet 2" in cleaned
    assert "\r" not in cleaned
    assert (
        "\n\n" not in cleaned
    )  # Blank lines should be stripped if they contain no text


def test_resume_detector_valid():
    """Tests resume heuristic detector with a valid resume text."""
    valid_resume_text = """
    John Doe
    john.doe@example.com | +1 (555) 123-4567 | linkedin.com/in/johndoe
    
    EXPERIENCE
    Software Engineer at TechFlow Inc.
    
    EDUCATION
    B.S. Computer Science
    
    SKILLS
    Python, AWS, Fastapi
    """
    assert is_valid_resume(valid_resume_text) is True


def test_resume_detector_invalid():
    """Tests resume heuristic detector with non-resume text (e.g. a recipe)."""
    recipe_text = """
    Pancakes Recipe
    Ingredients:
    - 1 cup flour
    - 2 eggs
    - 1 cup milk
    
    Instructions:
    Mix everything together and cook on a griddle.
    """
    with pytest.raises(NotAResumeException):
        is_valid_resume(recipe_text)


def test_hallucination_verifier_exact_match():
    """Tests verifier returning 'Verified' for exact substring."""
    original_text = "Worked as a Senior Backend Engineer at TechFlow Inc."
    extracted = "TechFlow Inc."

    result = verify_field(extracted, original_text)
    assert result is not None
    assert result.value == "TechFlow Inc."
    assert result.verification_state == "Verified"


def test_hallucination_verifier_partial_match():
    """Tests verifier returning 'Partially Verified' for disordered significant words."""
    original_text = "Worked as a Backend Engineer (Senior Level) at TechFlow Inc."
    extracted = "Senior Backend Engineer"

    result = verify_field(extracted, original_text)
    assert result is not None
    assert result.verification_state == "Partially Verified"


def test_hallucination_verifier_hallucinated():
    """Tests verifier returning 'Hallucinated' when no significant words exist."""
    original_text = "Worked as a Backend Engineer at TechFlow Inc."
    extracted = "AWS Solutions Architect"

    result = verify_field(extracted, original_text)
    assert result is not None
    assert result.verification_state == "Hallucinated"
