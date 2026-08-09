# ADR 0001: Use PostgreSQL for Foundation Architecture

## Status
Accepted

## Context
Merit AI currently uses SQLite for local development. However, the system requires a robust persistent storage solution capable of handling highly concurrent, asynchronous I/O operations and complex nested JSON data (Analysis Reports) for the future Recruiter Dashboard.

## Decision
We will transition the primary database to **PostgreSQL**.
- We will use **SQLAlchemy 2.0** with the **asyncpg** driver to maintain non-blocking asynchronous operations.
- We will use **Alembic** for schema migrations.
- We will NOT immediately deprecate SQLite; both configurations will temporarily coexist until PostgreSQL integration is fully validated across all API routes.

## Consequences
- **Positive:** PostgreSQL's `JSONB` support allows deep indexing of match reports without rigid relational mappings. `asyncpg` perfectly complements FastAPI's async event loop.
- **Negative:** Increased local development friction (requires Docker or a local Postgres instance).
