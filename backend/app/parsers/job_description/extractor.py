from app.exceptions.custom_exceptions import ParsingException
from app.parsers.resume.extractor import extract_text_from_docx, extract_text_from_pdf


def extract_text_from_txt(file_content: bytes) -> str:
    """Extracts text from a plain text file.

    Args:
        file_content: The binary content of the txt file.

    Returns:
        Extracted text as a string.

    Raises:
        ParsingException: If text decoding fails.
    """
    try:
        return file_content.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise ParsingException(
            "Failed to decode text file. Ensure it is UTF-8 encoded."
        )


def extract_jd_text(file_content: bytes, extension: str) -> str:
    """Routes the file to the appropriate text extractor based on its extension.

    Args:
        file_content: The binary content of the file.
        extension: The file extension (e.g., '.pdf', '.docx', '.txt').

    Returns:
        Extracted text as a string.
    """
    ext = extension.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_content)
    elif ext == ".docx":
        return extract_text_from_docx(file_content)
    elif ext == ".txt":
        return extract_text_from_txt(file_content)
    else:
        raise ParsingException(f"Unsupported extension for JD extraction: {extension}")
