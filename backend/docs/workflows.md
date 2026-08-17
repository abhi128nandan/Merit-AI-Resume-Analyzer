# System Workflows Document

## Phase 2 Workflow: Resume Upload & Validation

```text
User / Client
   │
   ├─► POST /api/v1/resumes/upload (Multipart File)
   │
   ▼
FastAPI API Transport Layer
   │
   ▼
File Validation Layer (app/validators/)
   ├─► File Extension Check (.pdf, .docx)
   ├─► MIME Type Check (application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document)
   ├─► File Size Boundaries (100 bytes <= size <= 5 MB)
   └─► Security Sanitization (Sanitize Filename & UUID Generation)
   │
   ▼
Safe Local Storage (app/services/ & uploads/)
   │
   ▼
JSON Success Response (Upload Metadata ID, Path, Status)
```

## Phase 3+ Future Workflows

1. **Resume Text Extraction**: Extracted via `pdfplumber` / `python-docx` into normalized string content.
2. **LLM Structuring**: Prompt engineering converts raw text to structured JSON schema (contact info, skills, experience, education).
3. **Matching & ATS Scoring**: Keyword overlap, missing hard skills, and experience relevancy scoring.
