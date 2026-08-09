# ADR 0003: Document Storage Strategy

## Status
Accepted

## Context
Merit AI ingests PDF and DOCX files for Resumes and Job Descriptions. We must define how these physical files are handled, stored, and persisted over time to support historical analysis and recruiter views.

## Decision
1. **Immediate Processing (In-Memory)**: Files uploaded to the `/analyze` endpoint will be read into memory directly and processed. They will *not* be saved to a local temporary disk unless absolutely required by a third-party parsing library.
2. **Long-Term Storage (Cloud Object Storage)**: To support the Recruiter Dashboard and Historical Analysis, physical files (PDF/DOCX) will eventually be uploaded to an Object Storage provider (e.g., AWS S3, Cloudflare R2, or MinIO). 
3. **Database Reference**: The PostgreSQL database will *not* store raw binaries. The `AnalysisReport`, `Resume`, and `JobDescription` tables will store URL references (or object keys) pointing to the S3 bucket.

## Consequences
- **Positive:** Keeps the database lean and performant. `JSONB` structures will hold the parsed text, while S3 handles the heavy binary blobs. Seamless scalability.
- **Negative:** Introduces a dependency on an object storage provider. Local development requires mocking the storage (or using local file system paths via an abstract Storage Adapter).
