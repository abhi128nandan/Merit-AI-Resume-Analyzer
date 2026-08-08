import re
import uuid
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """Sanitizes an incoming filename to prevent directory traversal."""
    safe_basename = Path(filename).name
    sanitized = re.sub(r"[^\w\.-]", "_", safe_basename)
    return sanitized


def generate_unique_filename(original_filename: str) -> str:
    """Generates a secure, unique filename preserving the original extension."""
    sanitized = sanitize_filename(original_filename)
    extension = Path(sanitized).suffix.lower()
    unique_id = uuid.uuid4().hex
    return f"{unique_id}{extension}"
