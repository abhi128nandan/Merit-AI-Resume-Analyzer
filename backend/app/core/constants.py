from typing import Set

# File Upload Limits
MAX_UPLOAD_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB
MIN_UPLOAD_SIZE_BYTES: int = 100  # 100 bytes minimum to reject empty files

# Allowed MIME Types and Extensions
ALLOWED_MIME_TYPES: Set[str] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

ALLOWED_FILE_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt"}

# Timeout and Retry Configurations
DEFAULT_TIMEOUT_SECONDS: int = 30
MAX_RETRY_LIMIT: int = 3

# Directory Configurations
DEFAULT_UPLOAD_DIR: str = "uploads"
DEFAULT_LOG_DIR: str = "logs"
