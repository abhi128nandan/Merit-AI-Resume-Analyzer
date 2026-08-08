import hashlib
from typing import Optional

from app.core.logging import logger
from app.schemas.parsed_resume import VerifiedParsedResume

# In-memory dictionary for V1. In production, this would be Redis.
_PARSE_CACHE: dict[str, VerifiedParsedResume] = {}


def generate_document_hash(text: str) -> str:
    """Generates a SHA-256 hash of the cleaned text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_cached_resume(text_hash: str) -> Optional[VerifiedParsedResume]:
    """Retrieves a parsed resume from the cache if it exists."""
    if text_hash in _PARSE_CACHE:
        logger.info(f"Cache HIT for hash {text_hash[:8]}...")
        return _PARSE_CACHE[text_hash]

    logger.info(f"Cache MISS for hash {text_hash[:8]}...")
    return None


def cache_parsed_resume(text_hash: str, parsed_resume: VerifiedParsedResume) -> None:
    """Stores a parsed resume in the cache."""
    _PARSE_CACHE[text_hash] = parsed_resume
    logger.info(f"Cached parsed resume for hash {text_hash[:8]}...")
