# ⚡ Merit AI — Backend API

Production-grade, asynchronous REST API built with **Python 3.12+** and **FastAPI**, engineered following Clean Architecture principles.

---

## Technical Highlights

- **Clean Architecture**: Strict separation of API routes, core settings, database connection, schemas, services, parsers, and matching logic.
- **Concurrent Parsing**: Offloaded CPU-bound PDF/DOCX text extractions to `ProcessPoolExecutor` using `asyncio.gather`.
- **Dual-Pass Hallucination Guard**: Cross-references LLM entity extractions against raw document source strings before score computation.
- **Deterministic ATS Matching Engine**: Hybrid scoring algorithm combining TF-IDF keyword overlap, semantic similarity, and rule-based policy weights.
- **Security Defenses**: Magic byte file validation, 5MB upload stream limits, UUID filename sanitization, and DoS mitigation.

---

## Project Structure

```text
backend/
├── app/
│   ├── api/v1/          # Versioned REST endpoints (/api/v1)
│   ├── core/            # Settings, constants, logging
│   ├── db/              # Database engine & session setup
│   ├── exceptions/      # Custom domain exceptions & handlers
│   ├── models/          # SQLAlchemy ORM entities
│   ├── schemas/         # Pydantic v2 DTOs
│   ├── services/        # Business orchestration layer
│   ├── parsers/         # Document extraction engines (Resume & JD)
│   ├── matching/        # ATS scoring engine & evidence extraction
│   ├── validators/      # Magic byte & file safety validators
│   └── main.py          # FastAPI application entry point
├── docs/                # System documentation
├── tests/               # Pytest suite & Red Team tests
├── requirements.txt     # Pinned Python dependencies
└── pyproject.toml       # Tooling configs (Black, isort, mypy, flake8, pytest)
```

---

## Quick Start (Backend Only)

```bash
cd backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload
```

Interactive API Docs:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testing & Quality Assurance

```bash
# Run pytest test suite
pytest

# Code Formatting & Type Verification
black app tests
isort app tests
flake8 app tests
mypy app tests
```

---

## Detailed Documentation
- [Architecture Overview](../docs/Architecture.md)
- [API Specification](../docs/API.md)
- [Matching Engine Mechanics](../docs/MatchingEngine.md)
- [Hallucination Guard](../docs/HallucinationGuard.md)
- [Security & Reliability](../docs/Security.md)
