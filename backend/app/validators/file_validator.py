from pathlib import Path

from app.core.constants import (
    ALLOWED_FILE_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    MAX_UPLOAD_SIZE_BYTES,
    MIN_UPLOAD_SIZE_BYTES,
)
from app.exceptions.custom_exceptions import (
    EmptyFileException,
    FileTooLargeException,
    InvalidFileUploadException,
    UnsupportedFileTypeException,
)


def validate_uploaded_file(
    filename: str,
    content_type: str,
    file_size: int,
    file_content: bytes,
) -> None:
    """Validates an uploaded file against extension, MIME type, size, and magic bytes rules.

    This is a pure validation function with no side effects.
    It raises a domain-specific exception on the first validation
    failure encountered. Returns None on success (no-news-is-good-news).

    Args:
        filename: The original filename from the upload.
        content_type: The MIME content type reported by the client.
        file_size: The size of the file content in bytes.
        file_content: The actual bytes of the file.

    Raises:
        InvalidFileUploadException: If the filename is missing.
        UnsupportedFileTypeException: If extension, MIME type, or magic bytes are invalid.
        EmptyFileException: If the file is empty or near-empty.
        FileTooLargeException: If the file exceeds the size limit.
    """
    # 1. Filename presence check
    if not filename or not filename.strip():
        raise InvalidFileUploadException(
            message="Filename is missing or empty.",
            details={"filename": filename},
        )

    # 2. Extension check
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_FILE_EXTENSIONS:
        raise UnsupportedFileTypeException(
            message=f"File extension '{extension}' is not supported.",
            details={
                "provided_extension": extension,
                "allowed_extensions": sorted(ALLOWED_FILE_EXTENSIONS),
            },
        )

    # 3. MIME type check
    if content_type not in ALLOWED_MIME_TYPES:
        raise UnsupportedFileTypeException(
            message=f"MIME type '{content_type}' is not supported.",
            details={
                "provided_mime_type": content_type,
                "allowed_mime_types": sorted(ALLOWED_MIME_TYPES),
            },
        )

    # 4. Magic Bytes check
    if extension == ".pdf":
        if not file_content.startswith(b"%PDF-"):
            raise UnsupportedFileTypeException(
                message="Invalid file format. File does not appear to be a valid PDF.",
                details={"expected_magic_bytes": "%PDF-"},
            )
    elif extension in [".doc", ".docx"]:
        # docx files are zip archives starting with PK
        # older .doc files use a different compound file binary format (D0 CF 11 E0)
        # We'll just check .docx for now since python-docx only supports docx
        if extension == ".docx" and not file_content.startswith(b"PK\x03\x04"):
            raise UnsupportedFileTypeException(
                message="Invalid file format. File does not appear to be a valid DOCX.",
                details={"expected_magic_bytes": "PK"},
            )
    elif extension == ".txt":
        try:
            file_content.decode("utf-8")
        except UnicodeDecodeError:
            raise UnsupportedFileTypeException(
                message="Invalid file format. Text file must be valid UTF-8 encoding.",
                details={"expected_encoding": "utf-8"},
            )

    # 5. Empty / near-empty file check
    if file_size < MIN_UPLOAD_SIZE_BYTES:
        raise EmptyFileException(
            message="Uploaded file is empty or too small.",
            details={
                "file_size_bytes": file_size,
                "minimum_size_bytes": MIN_UPLOAD_SIZE_BYTES,
            },
        )

    # 6. Oversized file check
    if file_size > MAX_UPLOAD_SIZE_BYTES:
        raise FileTooLargeException(
            message="Uploaded file exceeds the maximum allowed size.",
            details={
                "file_size_bytes": file_size,
                "max_size_bytes": MAX_UPLOAD_SIZE_BYTES,
            },
        )
