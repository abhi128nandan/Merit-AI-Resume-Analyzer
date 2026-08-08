# 📝 Changelog

All notable changes to **Merit AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-09

### Added
- **Clean Architecture Backend**: FastAPI REST backend with isolated presentation, domain, database, and parsing layers.
- **Next.js 16 Web Application**: Responsive interface built with Tailwind CSS v4, Framer Motion, and Radix UI primitives.
- **Concurrent Document Parser**: Multi-threaded PDF (`pdfplumber`) and DOCX (`python-docx`) parser offloading CPU tasks to `ProcessPoolExecutor`.
- **Deterministic ATS Matching Engine**: Hybrid scoring algorithm combining TF-IDF keyword overlap, semantic similarity, and rule-based domain policy weights.
- **Dual-Pass Hallucination Guard**: Two-pass verification pipeline eliminating LLM hallucinations by cross-referencing extracted JSON entities with raw document source strings.
- **Evidence Extraction**: Verbatim resume snippet isolation for every matched technical skill.
- **Security Defenses**: Magic byte MIME validation, maximum 5 MB payload stream limit, UUID filename sanitization, and DoS prevention controls.
- **Red Team Unit Tests**: Test suite covering security vulnerability scenarios, file traversal attacks, and malformed file handling.
- **Complete Developer & Recruiter Documentation**: Comprehensive documentation suite in `docs/` covering Architecture, API, Security, Matching Engine, Hallucination Guard, and Deployment.
