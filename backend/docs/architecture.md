# System Architecture Document

## Overview

The AI Resume Analyzer is built following Clean Architecture principles to separate API presentation, domain validation, document parsing, matching algorithms, database persistence, and LLM integrations into isolated packages.

## Directory Layout & Layer Responsibilities

- **`app/api/`**: Transport layer delivering REST endpoints (versioned under `v1/`).
- **`app/core/`**: Application configuration, system constants, centralized logging, and security utilities.
- **`app/db/`**: Database connection management, session creation (`database.py`), and base ORM model declarative base (`base.py`).
- **`app/exceptions/`**: Centralized custom exception definitions and global FastAPI exception handlers.
- **`app/models/`**: SQLAlchemy database entities (Users, Resumes, Analysis Reports).
- **`app/schemas/`**: Pydantic data transfer objects (DTOs) for request/response validation.
- **`app/services/`**: Business domain services orchestration layer.
- **`app/parsers/`**: Modular document extraction engines separated into `resume/` and `job_description/`.
- **`app/validators/`**: Input file, size, extension, MIME type, and payload safety validators.
- **`app/matching/`**: ATS keyword matching and skill scoring algorithms.
- **`app/prompts/`**: LLM prompt templates and engineering assets.
- **`app/utils/`**: Helper routines for date manipulation, file path management, and formatting.
