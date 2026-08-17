import hashlib
from typing import Optional

from app.core.logging import logger
from app.schemas.parsed_jd import VerifiedJD

_JD_CACHE: dict[str, VerifiedJD] = {}


def generate_jd_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_cached_jd(text_hash: str) -> Optional[VerifiedJD]:
    if text_hash in _JD_CACHE:
        logger.info(f"Cache HIT for JD hash {text_hash[:8]}...")
        return _JD_CACHE[text_hash]

    logger.info(f"Cache MISS for JD hash {text_hash[:8]}...")
    return None


def cache_parsed_jd(text_hash: str, parsed_jd: VerifiedJD) -> None:
    _JD_CACHE[text_hash] = parsed_jd
    logger.info(f"Cached parsed JD for hash {text_hash[:8]}...")
