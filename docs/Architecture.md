# 🏛️ Merit AI System Architecture

## Overview

Merit AI is designed around **Clean Architecture** principles to enforce strict boundary separation between API transport, input validation, parsing pipelines, deterministic semantic matching engines, and external LLM verification layers.

```mermaid
graph TD
    Client["Next.js 16 Web Frontend"] -->|"POST /api/v1/analyze<br>(Multipart Form)"| API["FastAPI Transport Layer"]
    API --> Val["File & Schema Validation Guard"]
    Val -->|"Sanitized Bytes"| Pipeline["Concurrent Document Pipeline"]
    
    subgraph "Parsing & Extraction Engine"
        Pipeline -->|"PDF Thread"| PDF["pdfplumber Extractor"]
        Pipeline -->|"DOCX Thread"| DOCX["python-docx Extractor"]
        PDF --> Detector["Section & Layout Detector"]
        DOCX --> Detector
        Detector --> Structurer["Schema Normalizer (Pydantic v2)"]
    end
    
    Structurer --> MatchEngine["Deterministic ATS Matching Engine"]
    
    subgraph "Matching & Scoring Subsystem"
        MatchEngine --> VectorSim["Cosine & Keyword Similarity"]
        MatchEngine --> Evidence["Evidence & Quote Mapper"]
        MatchEngine --> ScoringPolicy["Matching Policy Evaluator"]
    end
    
    ScoringPolicy --> Guard["Dual-Pass Hallucination Guard (LLM)"]
    Guard -->|"Verified JSON Report"| API
    API -->|"Typed JSON Response"| Client
```

---

## Component Breakdown

### 1. Presentation Layer (`frontend/`)
- **Framework**: Next.js 16 (App Router), React 19, TypeScript
- **Styling**: Tailwind CSS v4, Framer Motion, Radix UI primitives
- **State & Transport**: Client-side state machine with typed API abstraction ([`api.ts`](file:///d:/Apps/Resume_Analyzer/frontend/src/lib/api.ts))

### 2. Transport & Controller Layer (`backend/app/api/`)
- **Framework**: FastAPI (Async ASGI)
- **Versioning**: Prefix-based route versioning (`/api/v1`)
- **Exception Handling**: Global exception interceptor (`app/exceptions/handlers.py`) returning uniform JSON payloads:
  ```json
  {
    "error": {
      "code": "INVALID_FILE_TYPE",
      "message": "File extension .exe is not permitted",
      "details": null
    }
  }
  ```

### 3. Parsing Subsystem (`backend/app/parsers/`)
- Isolated parsers for resumes (`app/parsers/resume/`) and job descriptions (`app/parsers/job_description/`)
- Multi-threaded text extraction offloaded to `ProcessPoolExecutor` via `asyncio.gather`
- Layout detection algorithm isolates Work Experience, Technical Skills, Education, and Projects

### 4. Matching & ATS Engine (`backend/app/matching/`)
- **Similarity Computation**: TF-IDF keyword overlap + semantic embedding vector scoring
- **Evidence Collector**: Extracts verbatim supporting text snippets from the resume for each required skill
- **Policy Matrix**: Configurable domain weights (Hard Skills: 40%, Experience Relevancy: 30%, Tooling: 20%, Education: 10%)

### 5. Dual-Pass Hallucination Guard (`backend/app/parsers/*/verifier.py`)
- Pass 1: Extraction & Structuring via LLM
- Pass 2: Fact-checking verifier cross-references LLM outputs against source document raw strings before score finalization

---

## Data Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FE as Next.js Frontend
    participant API as FastAPI /api/v1/analyze
    participant Val as File Validator
    participant Engine as Parsing & Matching Pipeline
    participant LLM as LLM Verifier (Groq/Gemini)

    User->>FE: Upload Resume (PDF/DOCX) + Paste Job Description
    FE->>API: POST /api/v1/analyze (multipart/form-data)
    API->>Val: Validate MIME, File Size (<5MB), & Filename Safety
    Val-->>API: Validated
    API->>Engine: Dispatch to ProcessPoolExecutor
    Engine->>Engine: Extract raw text & section boundaries
    Engine->>LLM: Pass 1: Extract structured JSON (Skills, Years, Experience)
    LLM-->>Engine: Raw Structured JSON
    Engine->>LLM: Pass 2: Fact-Check verbatim quotes vs source text
    LLM-->>Engine: Verified Ground-Truth Payload
    Engine->>Engine: Run Matching Engine & Compute ATS Score (0-100)
    Engine-->>API: AnalysisReport Schema
    API-->>FE: HTTP 200 JSON Response
    FE-->>User: Render Interactive ATS Dashboard
```

---

## Further Reading
- [API Specification](API.md)
- [Matching Engine & Scoring Logic](MatchingEngine.md)
- [Hallucination Guard Mechanics](HallucinationGuard.md)
- [Security Specifications](Security.md)
