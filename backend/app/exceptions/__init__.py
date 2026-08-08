"""Exceptions package."""

from app.exceptions.custom_exceptions import (
    EmptyFileException,
    FileTooLargeException,
    InvalidFileUploadException,
    LLMIntegrationException,
    ParsingException,
    ResumeAnalyzerException,
    UnsupportedFileTypeException,
    ValidationException,
)
from app.exceptions.handlers import register_exception_handlers

__all__ = [
    "ResumeAnalyzerException",
    "InvalidFileUploadException",
    "UnsupportedFileTypeException",
    "FileTooLargeException",
    "EmptyFileException",
    "ParsingException",
    "ValidationException",
    "LLMIntegrationException",
    "register_exception_handlers",
]
