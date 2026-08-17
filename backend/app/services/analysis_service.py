import asyncio
import time
import uuid
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone

from app.core.context import correlation_id_ctx
from app.core.logging import logger
from app.exceptions.custom_exceptions import ParsingException, ResumeAnalyzerException
from app.matching.engine import evaluate_match
from app.matching.policies import DEFAULT_POLICY
from app.parsers.job_description.pipeline import process_job_description
from app.parsers.resume.pipeline import process_resume
from app.schemas.analysis import AnalysisFeedback, AnalysisMetadata, AnalysisResponse

# A dedicated ProcessPool for CPU-intensive document parsing.
# We limit workers to avoid memory exhaustion from concurrent pdfplumber instances.
_executor = ProcessPoolExecutor(max_workers=4)


def generate_correlation_id() -> str:
    """Generates a standard ANL correlation ID (e.g. ANL-20260808-183015-001)"""
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y%m%d-%H%M%S")
    # Taking first 4 chars of UUID for uniqueness in the same second
    short_uuid = str(uuid.uuid4())[:4]
    return f"ANL-{date_str}-{short_uuid}"


async def run_pipeline_with_timeout(func, timeout: int, *args):
    """Executes a synchronous CPU/IO task in the ProcessPool with a hard timeout."""
    loop = asyncio.get_running_loop()
    try:
        # Submit task to ProcessPool to prevent blocking the FastAPI event loop
        future = loop.run_in_executor(_executor, func, *args)
        return await asyncio.wait_for(future, timeout=timeout)
    except asyncio.TimeoutError:
        logger.error(f"Task {func.__name__} timed out after {timeout} seconds.")
        raise
    except Exception as e:
        logger.error(f"Task {func.__name__} failed: {str(e)}")
        raise


def _generate_ai_feedback(match_report) -> AnalysisFeedback:
    """Generates actionable feedback based on the match report.
    In V1, this is a deterministic generation based on the matching engine's evidence.
    In V2, this could be delegated to an LLM.
    """
    matched = []
    missing = []

    # Extract from skills evaluation
    for ev in match_report.skills_evaluation.evidence:
        if ev.match_level in ["Exact", "Semantic", "Partial"]:
            matched.append(ev.requirement)
        elif ev.match_level == "Missing":
            missing.append(ev.requirement)

    suggestions = []
    if missing:
        suggestions.append(f"Consider acquiring skills in: {', '.join(missing[:3])}")
    if match_report.overall_score < 70:
        suggestions.append(
            "Tailor your resume terminology to better match the job description."
        )

    return AnalysisFeedback(
        matched_skills=matched,
        missing_skills=missing,
        improvement_suggestions=suggestions,
        warnings=(
            ["Low confidence in some extracted fields."]
            if match_report.confidence_warning
            else []
        ),
    )


async def execute_analysis_workflow(
    resume_bytes: bytes, resume_filename: str, jd_bytes: bytes, jd_filename: str
) -> AnalysisResponse:
    """
    The master orchestration workflow.

    Timeouts:
    - Resume Parsing: 10s
    - JD Parsing: 10s
    - Matching: 2s
    Total budget: ~15s (since parsing is concurrent)
    """
    start_time = time.time()

    analysis_id = generate_correlation_id()
    correlation_id_ctx.set(analysis_id)

    logger.info(f"[{analysis_id}] Initiating Analysis Workflow")

    # 1. Concurrent Parsing (Timeout: 25 seconds)
    try:
        resume_task = run_pipeline_with_timeout(
            process_resume, 25, resume_bytes, resume_filename
        )
        jd_task = run_pipeline_with_timeout(
            process_job_description, 25, jd_bytes, jd_filename
        )

        # return_exceptions=False means if one fails, gather throws immediately.
        # This is desired, as we cannot continue without both.
        parsed_resume, parsed_jd = await asyncio.gather(resume_task, jd_task)
    except asyncio.TimeoutError:
        logger.error(f"[{analysis_id}] Pipeline Timeout Exceeded.")
        raise ResumeAnalyzerException(
            "Processing timeout exceeded. Documents are too complex.", status_code=504
        )
    except ParsingException as e:
        logger.error(
            f"[{analysis_id}] Pipeline failed due to invalid document: {e.message}"
        )
        raise  # Let the router catch and return 422
    except Exception as e:
        logger.critical(f"[{analysis_id}] Unexpected pipeline crash: {str(e)}")
        raise ResumeAnalyzerException(
            "An unexpected error occurred during processing.", status_code=500
        )

    # 2. Matching Engine (Timeout: 2 seconds)
    try:
        loop = asyncio.get_running_loop()
        # evaluate_match is synchronous math. We can run it in default executor if it's CPU intensive,
        # but it's very fast math. We'll run it directly but enforce a timeout just in case.
        match_task = loop.run_in_executor(
            None, evaluate_match, parsed_resume, parsed_jd, DEFAULT_POLICY
        )
        match_report = await asyncio.wait_for(match_task, timeout=2.0)
    except Exception as e:
        logger.critical(f"[{analysis_id}] Matching Engine Failure: {str(e)}")
        # Failsafe: We cannot return a score if matching crashes.
        raise ResumeAnalyzerException("Failed to calculate ATS score.", status_code=500)

    # 3. AI Feedback
    feedback = _generate_ai_feedback(match_report)

    # 4. Construct Response
    processing_time_ms = int((time.time() - start_time) * 1000)
    logger.info(
        f"[{analysis_id}] Workflow Completed in {processing_time_ms}ms with score {match_report.overall_score}"
    )

    metadata = AnalysisMetadata(
        analysis_id=analysis_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        processing_time_ms=processing_time_ms,
        parser_version="1.2.0",
        policy_version="default-v1",
    )

    return AnalysisResponse(
        metadata=metadata,
        parsed_resume=parsed_resume,
        parsed_jd=parsed_jd,
        match_report=match_report,
        feedback=feedback,
    )
