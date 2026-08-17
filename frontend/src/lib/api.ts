// src/lib/api.ts

export interface AnalysisMetadata {
  analysis_id: string;
  generated_at: string;
  processing_time_ms: number;
  parser_version: string;
  policy_version: string;
}

export interface VerificationState {
  value: string | number | null;
  verification_state: string;
}

export interface VerifiedParsedResume {
  contact: Record<string, VerificationState | null>;
  summary?: VerificationState;
  skills: VerificationState[];
  experience: Record<string, unknown>[];
  education: Record<string, unknown>[];
  overall_confidence: number;
  section_confidence: Record<string, number>;
}

export interface VerifiedJD {
  job_title: VerificationState;
  company: VerificationState;
  location: VerificationState;
  employment_type: VerificationState;
  required_skills: VerificationState[];
  preferred_skills: VerificationState[];
  responsibilities: VerificationState[];
  qualifications: VerificationState[];
  experience_requirements: VerificationState;
  education_requirements: VerificationState;
  overall_confidence: number;
  section_confidence: Record<string, number>;
}

export interface EvidenceResult {
  requirement: string;
  match_level: string; // "Exact", "Semantic", "Partial", "Weak", "Missing", "Hallucinated"
  evidence: string;
  score_contribution: number;
}

export interface MatchCategoryResult {
  score: number;
  evidence: EvidenceResult[];
}

export interface MatchReport {
  overall_score: number;
  skills_evaluation: MatchCategoryResult;
  experience_evaluation: MatchCategoryResult;
  education_evaluation: MatchCategoryResult;
  title_evaluation: MatchCategoryResult;
  confidence_warning: boolean;
}

export interface AnalysisFeedback {
  matched_skills: string[];
  missing_skills: string[];
  improvement_suggestions: string[];
  warnings: string[];
}

export interface AnalysisResponse {
  metadata: AnalysisMetadata;
  parsed_resume: VerifiedParsedResume;
  parsed_jd: VerifiedJD;
  match_report: MatchReport;
  feedback: AnalysisFeedback;
}

export class ApiError extends Error {
  constructor(public status: number, public message: string, public details?: unknown) {
    super(message);
    this.name = "ApiError";
  }
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function analyzeMatch(resumeFile: File, jdText: string): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  
  // Create a blob from the JD text to send as a file
  const jdBlob = new Blob([jdText], { type: "text/plain" });
  const jdFile = new File([jdBlob], "jd.txt", { type: "text/plain" });
  formData.append("jd", jdFile);

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      body: formData,
      // Note: Do NOT set Content-Type header when using FormData. The browser will set it automatically with the boundary.
      credentials: "include",
    });

    if (!response.ok) {
      let errorMessage = "An unexpected error occurred.";
      let errorDetails = null;

      try {
        const errorData = await response.json();
        if (errorData.error) {
          errorMessage = errorData.error.message || errorMessage;
          errorDetails = errorData.error.details || null;
        } else if (errorData.detail) {
          // Fallback for standard FastAPI validation errors
          if (Array.isArray(errorData.detail)) {
             errorMessage = "Validation Error: " + errorData.detail.map((d: { msg?: string }) => d.msg || "").join(", ");
          } else {
             errorMessage = String(errorData.detail);
          }
        }
      } catch {
         if (response.status === 413) errorMessage = "The uploaded file exceeds the 5 MB limit.";
         if (response.status === 422) errorMessage = "This file is not a valid resume or document structure.";
         if (response.status === 504) errorMessage = "The analysis timed out.";
         if (response.status === 500) errorMessage = "Internal processing failed. Please try again.";
      }

      throw new ApiError(response.status, errorMessage, errorDetails);
    }

    const data: AnalysisResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Handle network errors (e.g. CORS failure, backend down)
    throw new ApiError(0, "Failed to connect to the analysis server. Please check your connection or try again later.");
  }
}

// --- Auth Endpoints ---

export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
    credentials: "include",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(response.status, errorData.detail || "Invalid email or password");
  }
  return response.json();
}

export async function register(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(response.status, errorData.detail || "Registration failed");
  }
  return response.json();
}

export async function logout() {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "Logout failed");
  }
  return response.json();
}

export async function getMe() {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    credentials: "include",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "Not authenticated");
  }
  return response.json();
}

// --- History Endpoints ---

export interface HistoryItem {
  id: string;
  resume_filename: string;
  jd_filename: string;
  overall_score: number;
  created_at: string;
}

export async function getHistory(): Promise<HistoryItem[]> {
  const response = await fetch(`${API_BASE_URL}/history/`, {
    method: "GET",
    credentials: "include",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "Failed to fetch history");
  }
  return response.json();
}

export async function getAnalysis(id: string): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/history/${id}`, {
    method: "GET",
    credentials: "include",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "Failed to fetch analysis");
  }
  return response.json();
}

export async function deleteAnalysis(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/history/${id}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!response.ok) {
    throw new ApiError(response.status, "Failed to delete analysis");
  }
}
