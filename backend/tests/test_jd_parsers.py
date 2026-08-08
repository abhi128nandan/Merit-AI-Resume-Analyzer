import pytest
from app.exceptions.custom_exceptions import NotAJobDescriptionException
from app.parsers.job_description.detector import is_valid_jd
from app.parsers.job_description.extractor import extract_text_from_txt


def test_txt_extractor_valid_utf8():
    """Tests that a valid UTF-8 txt file is extracted correctly."""
    valid_bytes = b"Job Title: Senior Backend Engineer\nRequirements: Python"
    text = extract_text_from_txt(valid_bytes)
    assert text == "Job Title: Senior Backend Engineer\nRequirements: Python"


def test_jd_detector_valid():
    """Tests deterministic JD detector with a valid JD text."""
    valid_jd_text = """
    Job Title: Senior Backend Engineer
    Company: TechFlow Inc.
    
    Responsibilities:
    - Build microservices.
    
    Requirements:
    - 5+ years of experience in backend development.
    - Python and FastAPI.
    
    Employment Type: Full-time
    """
    assert is_valid_jd(valid_jd_text) is True


def test_jd_detector_invalid():
    """Tests JD detector with non-JD text (e.g., a recipe)."""
    recipe_text = """
    Pancakes Recipe
    Ingredients:
    - 1 cup flour
    - 2 eggs
    - 1 cup milk
    
    Instructions:
    Mix everything together and cook on a griddle.
    """
    with pytest.raises(NotAJobDescriptionException):
        is_valid_jd(recipe_text)


def test_jd_detector_resume():
    """Tests JD detector with a resume text (should fail if it lacks JD markers like requirements, responsibilities)."""
    resume_text = """
    John Doe
    john.doe@example.com
    
    EXPERIENCE
    Software Engineer at TechFlow Inc.
    - Wrote Python code.
    
    EDUCATION
    B.S. Computer Science
    """
    with pytest.raises(NotAJobDescriptionException):
        is_valid_jd(resume_text)
