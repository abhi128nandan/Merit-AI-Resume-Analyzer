from typing import Any, Dict, Optional


class ResumeAnalyzerException(Exception):
    """Base exception for all domain-specific errors in AI Resume Analyzer."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class InvalidFileUploadException(ResumeAnalyzerException):
    """Raised when an uploaded file fails baseline structural validation."""

    def __init__(
        self,
        message: str = "Invalid file upload.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class UnsupportedFileTypeException(ResumeAnalyzerException):
    """Raised when an uploaded file extension or MIME type is not supported."""

    def __init__(
        self,
        message: str = "Unsupported file type.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=415, details=details)


class FileTooLargeException(ResumeAnalyzerException):
    """Raised when an uploaded file exceeds maximum permissible size limit."""

    def __init__(
        self,
        message: str = "File size exceeds allowed limit.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=413, details=details)


class EmptyFileException(ResumeAnalyzerException):
    """Raised when an uploaded file is empty (0 bytes)."""

    def __init__(
        self,
        message: str = "Uploaded file is empty.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class ParsingException(ResumeAnalyzerException):
    """Raised when document parsing (PDF/DOCX) fails."""

    def __init__(
        self,
        message: str = "Failed to parse document content.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class ValidationException(ResumeAnalyzerException):
    """Raised when payload or domain validation fails."""

    def __init__(
        self,
        message: str = "Validation error.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class LLMIntegrationException(ResumeAnalyzerException):
    """Raised when downstream LLM processing fails or encounters invalid output."""

    def __init__(
        self,
        message: str = "LLM processing error.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=502, details=details)


class PasswordProtectedPDFException(ResumeAnalyzerException):
    """Raised when an uploaded PDF is password protected."""

    def __init__(
        self,
        message: str = "Your resume is password protected. Please remove the password and try again.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class NotAResumeException(ResumeAnalyzerException):
    """Raised when the document heuristic score implies it's not a resume."""

    def __init__(
        self,
        message: str = "Document does not appear to be a valid resume.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class NotAJobDescriptionException(ResumeAnalyzerException):
    """Raised when the document heuristic score implies it's not a job description."""

    def __init__(
        self,
        message: str = "Document does not appear to be a valid job description.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)


class VerificationException(ResumeAnalyzerException):
    """Raised when LLM output cannot be verified against the source text."""

    def __init__(
        self,
        message: str = "Some extracted data could not be verified.",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=422, details=details)
