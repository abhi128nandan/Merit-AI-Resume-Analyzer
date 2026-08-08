from pathlib import Path

from fastapi import UploadFile

from app.core.constants import DEFAULT_UPLOAD_DIR, MAX_UPLOAD_SIZE_BYTES
from app.core.logging import logger
from app.core.security import generate_unique_filename, sanitize_filename
from app.exceptions.custom_exceptions import FileTooLargeException
from app.schemas.resume import ResumeUploadResponse
from app.validators.file_validator import validate_uploaded_file


async def save_uploaded_file(file: UploadFile) -> ResumeUploadResponse:
    """Orchestrates the resume upload flow: validate, store, and respond.

    This service reads the file content, validates it against all safety
    constraints, writes it to disk with a UUID-based filename, and
    returns a structured response DTO.

    Args:
        file: The FastAPI UploadFile received from the multipart form.

    Returns:
        ResumeUploadResponse with upload metadata.

    Raises:
        Domain exceptions from file_validator on validation failure.
    """
    # 1. Read file content safely in chunks to prevent OOM / DoS
    file_size = 0
    content_chunks = []

    # Read in 1MB chunks
    while chunk := await file.read(1024 * 1024):
        file_size += len(chunk)
        # Fail fast if file exceeds max size during read
        if file_size > MAX_UPLOAD_SIZE_BYTES:
            raise FileTooLargeException(
                message="Uploaded file exceeds the maximum allowed size.",
                details={
                    "file_size_bytes": file_size,
                    "max_size_bytes": MAX_UPLOAD_SIZE_BYTES,
                },
            )
        content_chunks.append(chunk)

    content = b"".join(content_chunks)

    # 2. Resolve filename and content type
    original_filename = file.filename or "unknown"
    content_type = file.content_type or "application/octet-stream"

    logger.info(
        f"Upload received: filename='{original_filename}', "
        f"content_type='{content_type}', size={file_size} bytes"
    )

    # 3. Validate (raises domain exception on failure)
    validate_uploaded_file(
        filename=original_filename,
        content_type=content_type,
        file_size=file_size,
        file_content=content,
    )

    # 4. Generate safe storage filename
    sanitized_name = sanitize_filename(original_filename)
    stored_filename = generate_unique_filename(original_filename)
    file_id = Path(stored_filename).stem  # UUID portion

    # 5. Ensure upload directory exists and write file
    upload_dir = Path(DEFAULT_UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / stored_filename

    with open(file_path, "wb") as f:
        f.write(content)

    logger.info(f"Upload stored: file_id='{file_id}', " f"path='{file_path}'")

    # 6. Build and return response
    return ResumeUploadResponse(
        file_id=file_id,
        original_filename=sanitized_name,
        stored_filename=stored_filename,
        file_size=file_size,
        content_type=content_type,
        status="uploaded",
    )
