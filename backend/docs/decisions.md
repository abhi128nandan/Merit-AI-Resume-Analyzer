# Architectural Decision Log (ADR)

## ADR 001: Centralized Configuration Management
* **Status**: Accepted
* **Context**: Need a single, type-safe settings module accessible across the app without reading `.env` multiple times.
* **Decision**: Implemented `app/core/config.py` leveraging `python-dotenv`.
* **Impact**: Centralizes `DATABASE_URL`, API keys, log level, and environment settings.

## ADR 002: Dedicated Database Layer (`app/db`)
* **Status**: Accepted
* **Context**: Database configuration should not be mixed into ORM model definitions.
* **Decision**: Isolated `database.py` (engine, session maker, `get_db`) and `base.py` (`Base = declarative_base()`) in `app/db/`.
* **Impact**: Prevents circular imports and cleanly decouples session dependency injection from domain entities.

## ADR 003: Versioned REST Routing (`app/api/v1`)
* **Status**: Accepted
* **Context**: System needs to support backward-compatible API evolution.
* **Decision**: Grouped endpoints under `app/api/v1/endpoints` attached to `api_v1_router` under `/api/v1`.
* **Impact**: Enables future `/api/v2` additions without breaking v1 clients.

## ADR 004: Centralized Exception Architecture & Handlers
* **Status**: Accepted
* **Context**: Need unified error payload formats and prevent unhandled standard Python exceptions from leaking stack traces.
* **Decision**: Created `app/exceptions/custom_exceptions.py` deriving from `ResumeAnalyzerException` and `handlers.py` registered globally in `main.py`.
* **Impact**: All errors return a predictable JSON payload format: `{"error": {"code": ..., "message": ..., "details": ...}}`.
