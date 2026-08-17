import pathlib

from app.core.logging import logger
from app.parsers.resume.cache import (
    cache_parsed_resume,
    generate_document_hash,
    get_cached_resume,
)
from app.parsers.resume.cleaner import clean_extracted_text
from app.parsers.resume.detector import is_valid_resume
from app.parsers.resume.extractor import extract_text
from app.parsers.resume.llm_parser import parse_resume_with_llm
from app.parsers.resume.verifier import verify_resume_data
from app.schemas.parsed_resume import VerifiedParsedResume


def process_resume(file_content: bytes, filename: str) -> VerifiedParsedResume:
    """Orchestrates the complete document parsing pipeline.

    Pipeline Steps:
    1. Text Extraction (pdfplumber / python-docx)
    2. Text Cleaning & Normalization
    3. Resume Detection (Deterministic Heuristic)
    4. Cache Lookup (SHA-256 of cleaned text)
    5. LLM Semantic Structuring
    6. Hallucination Verification & Confidence Scoring
    7. Caching

    Args:
        file_content: The binary content of the validated file.
        filename: The original filename to determine extension.

    Returns:
        VerifiedParsedResume containing the structured data and confidence scores.
    """
    logger.info(f"Starting parsing pipeline for {filename}")

    extension = pathlib.Path(filename).suffix.lower()

    # Step 1: Extract
    raw_text = extract_text(file_content, extension)
    logger.info(f"Extracted {len(raw_text)} characters.")

    # Step 2: Clean
    cleaned_text = clean_extracted_text(raw_text)
    logger.info(f"Cleaned text to {len(cleaned_text)} characters.")

    # Step 3: Detect
    is_valid_resume(cleaned_text)  # Raises exception if invalid

    # Step 4: Cache Lookup
    text_hash = generate_document_hash(cleaned_text)
    cached_resume = get_cached_resume(text_hash)
    if cached_resume:
        return cached_resume

    # Step 5: LLM Extraction
    llm_output = parse_resume_with_llm(cleaned_text)

    # Step 6: Verify and Score
    verified_resume = verify_resume_data(llm_output, cleaned_text)
    logger.info(
        f"Verification complete. Overall confidence: {verified_resume.overall_confidence}%"
    )

    # Step 7: Cache Result
    cache_parsed_resume(text_hash, verified_resume)

    return verified_resume
