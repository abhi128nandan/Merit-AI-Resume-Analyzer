import pathlib

from app.core.logging import logger

from app.parsers.job_description.detector import is_valid_jd
from app.parsers.job_description.extractor import extract_jd_text
from app.parsers.job_description.llm_parser import parse_jd_with_llm
from app.parsers.job_description.verifier import verify_jd_data
from app.parsers.resume.cleaner import clean_extracted_text
from app.schemas.parsed_jd import VerifiedJD


def process_job_description(file_content: bytes, filename: str) -> VerifiedJD:
    """Orchestrates the complete JD document parsing pipeline.

    Pipeline Steps:
    1. Text Extraction (.txt, .pdf, .docx)
    2. Text Cleaning & Normalization (reused from resume cleaner)
    3. JD Detection (Deterministic Heuristic)
    4. LLM Semantic Structuring
    5. Hallucination Verification & Confidence Scoring

    Args:
        file_content: The binary content of the validated file.
        filename: The original filename to determine extension.

    Returns:
        VerifiedJD containing structured data and confidence scores.
    """
    logger.info(f"Starting JD parsing pipeline for {filename}")

    extension = pathlib.Path(filename).suffix.lower()

    # Step 1: Extract
    raw_text = extract_jd_text(file_content, extension)
    logger.info(f"Extracted {len(raw_text)} characters.")

    # Step 2: Clean
    cleaned_text = clean_extracted_text(raw_text)
    logger.info(f"Cleaned JD text to {len(cleaned_text)} characters.")

    # Step 3: Detect
    is_valid_jd(cleaned_text)


    # Step 5: LLM Extraction
    llm_output = parse_jd_with_llm(cleaned_text)

    # Step 6: Verify and Score
    verified_jd = verify_jd_data(llm_output, cleaned_text)
    logger.info(
        f"Verification complete. Overall JD confidence: {verified_jd.overall_confidence}%"
    )


    return verified_jd
