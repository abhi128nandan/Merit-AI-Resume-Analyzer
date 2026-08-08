from app.matching.evidence import (
    collect_education_evidence,
    collect_experience_evidence,
    collect_skills_evidence,
    collect_title_evidence,
)
from app.matching.policies import DEFAULT_POLICY, MatchingPolicy
from app.matching.report import generate_match_report
from app.matching.scorer import score_category, score_skills
from app.schemas.match_report import MatchReport
from app.schemas.parsed_jd import VerifiedJD
from app.schemas.parsed_resume import VerifiedParsedResume


def evaluate_match(
    resume: VerifiedParsedResume,
    jd: VerifiedJD,
    policy: MatchingPolicy = DEFAULT_POLICY,
) -> MatchReport:
    """The central orchestrator for the ATS Matching Engine.

    1. Collects evidence for each requirement (Skills, Experience, Education, Title)
    2. Filters out hallucinated data points.
    3. Scores the collected evidence using the provided MatchingPolicy.
    4. Generates a comprehensive MatchReport.
    """

    # 1. Check for overarching confidence issues
    has_hallucinations = False
    if resume.overall_confidence < 80 or jd.overall_confidence < 80:
        has_hallucinations = True

    # 2. Collect Evidence
    req_skills_evidence = collect_skills_evidence(resume, jd, is_required=True)
    pref_skills_evidence = collect_skills_evidence(resume, jd, is_required=False)

    exp_evidence = collect_experience_evidence(resume, jd)
    edu_evidence = collect_education_evidence(resume, jd)
    title_evidence = collect_title_evidence(resume, jd)

    # 3. Score Evidence
    skills_eval = score_skills(req_skills_evidence, pref_skills_evidence, policy)
    exp_eval = score_category(exp_evidence, policy)
    edu_eval = score_category(edu_evidence, policy)
    title_eval = score_category(title_evidence, policy)

    # 4. Generate Final Report
    report = generate_match_report(
        skills_eval=skills_eval,
        exp_eval=exp_eval,
        edu_eval=edu_eval,
        title_eval=title_eval,
        policy=policy,
        has_hallucinations=has_hallucinations,
    )

    return report
