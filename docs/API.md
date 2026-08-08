# 🔌 Merit AI API Documentation

## Base Specification

- **Protocol**: HTTP / 1.1 & HTTP / 2
- **Data Format**: `application/json` (Multipart Form Data for File Uploads)
- **Base URL**: `/api/v1`
- **Interactive OpenAPI Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc Specification**: `http://localhost:8000/redoc`

---

## Endpoints Summary

| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/` | Root API Metadata & Docs Pointer | No |
| `GET` | `/api/v1/health` | System & DB Health Check | No |
| `POST` | `/api/v1/resumes/upload` | Upload & validate resume document | No |
| `POST` | `/api/v1/analyze` | Full ATS analysis (Resume + Job Description) | No |

---

## Endpoint Details

### 1. System Health Check

#### Request
```http
GET /api/v1/health HTTP/1.1
Host: localhost:8000
Accept: application/json
```

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-08-09T01:42:00Z"
}
```

---

### 2. Full ATS Resume Analysis

Performs end-to-end parsing, skill extraction, ATS keyword matching, evidence isolation, and feedback generation.

#### Request
```http
POST /api/v1/analyze HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="resume"; filename="candidate_resume.pdf"
Content-Type: application/pdf

(Binary PDF Content)
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="job_description"

We are looking for a Senior Python Developer with FastAPI, PostgreSQL, and Docker experience...
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

#### Request Constraints
- `resume`: PDF or DOCX file, maximum size **5 MB**
- `job_description`: Plain text string (minimum 50 characters, maximum 10,000 characters)

#### Response (`200 OK`)
```json
{
  "overall_score": 84,
  "match_breakdown": {
    "hard_skills_score": 90,
    "experience_relevancy_score": 80,
    "tooling_score": 85,
    "education_score": 75
  },
  "matched_skills": [
    {
      "skill": "Python",
      "category": "Programming Languages",
      "evidence_quote": "5+ years of production experience building Python backends.",
      "confidence": 0.98
    },
    {
      "skill": "FastAPI",
      "category": "Frameworks",
      "evidence_quote": "Architected RESTful microservices using FastAPI and Pydantic.",
      "confidence": 0.95
    }
  ],
  "missing_skills": [
    {
      "skill": "Docker",
      "category": "DevOps",
      "importance": "High",
      "recommendation": "Highlight containerization experience or add Docker projects."
    }
  ],
  "executive_summary": "Strong technical alignment for senior backend roles. High proficiency in Python frameworks with minor gaps in container orchestration tools.",
  "actionable_recommendations": [
    "Quantify impact in work experience bullet points.",
    "Explicitly mention container deployments if applicable."
  ]
}
```

---

## Error Handling Matrix

All endpoints respond with standardized RFC 7807 compliant error payloads:

```json
{
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "File size exceeds the maximum limit of 5.0 MB",
    "details": {
      "file_size_bytes": 7482910,
      "max_bytes": 5242880
    }
  }
}
```

| HTTP Status | Error Code | Root Cause |
|:---:|---|---|
| `400 Bad Request` | `INVALID_FILE_EXTENSION` | File extension is not `.pdf` or `.docx` |
| `400 Bad Request` | `MIME_TYPE_MISMATCH` | Magic bytes do not match declared header |
| `413 Payload Too Large` | `FILE_TOO_LARGE` | File size > 5 MB |
| `422 Unprocessable Entity` | `JD_TOO_SHORT` | Job description length < 50 characters |
| `500 Internal Error` | `PARSER_FAILURE` | Text extraction engine failure |
| `503 Service Unavailable` | `LLM_RATE_LIMIT` | Upstream AI service unavailable |
