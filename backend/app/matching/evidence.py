from typing import List

from app.matching.similarity import evaluate_similarity, extract_years_of_experience
from app.schemas.match_report import EvidenceResult, MatchLevel
from app.schemas.parsed_jd import VerifiedJD
from app.schemas.parsed_resume import VerifiedParsedResume


def collect_skills_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD, is_required: bool
) -> List[EvidenceResult]:
    """Collects evidence for skills matching."""
    evidence_list = []
    jd_skills = jd.required_skills if is_required else jd.preferred_skills

    # Extract all text from verified skills on resume
    resume_skills = [
        s.value for s in resume.skills if s.verification_state != "Hallucinated"
    ]

    for req in jd_skills:
        if req.verification_state == "Hallucinated":
            continue

        best_match_level = MatchLevel.MISSING
        best_match_text = None

        for r_skill in resume_skills:
            level = evaluate_similarity(r_skill, req.value)

            # Prioritize Exact > Semantic > Partial > Weak
            if level == MatchLevel.EXACT:
                best_match_level = MatchLevel.EXACT
                best_match_text = r_skill
                break
            elif level == MatchLevel.SEMANTIC and best_match_level not in [
                MatchLevel.EXACT
            ]:
                best_match_level = MatchLevel.SEMANTIC
                best_match_text = r_skill
            elif level == MatchLevel.PARTIAL and best_match_level not in [
                MatchLevel.EXACT,
                MatchLevel.SEMANTIC,
            ]:
                best_match_level = MatchLevel.PARTIAL
                best_match_text = r_skill
            elif level == MatchLevel.WEAK and best_match_level == MatchLevel.MISSING:
                best_match_level = MatchLevel.WEAK
                best_match_text = r_skill

        evidence_list.append(
            EvidenceResult(
                requirement=req.value,
                match_level=best_match_level,
                evidence_found=best_match_text,
            )
        )

    return evidence_list


def collect_experience_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    """Collects evidence for experience matching."""
    if jd.experience_requirements.verification_state == "Hallucinated":
        return []

    req_years = extract_years_of_experience(jd.experience_requirements.value)

    # Calculate candidate total years
    candidate_years = 0
    evidence_texts = []

    for exp in resume.experience:
        if exp.title.verification_state != "Hallucinated":
            # Very naive mock calculation for V1 based on text
            start = extract_years_of_experience(exp.start_date.value)
            end = extract_years_of_experience(exp.end_date.value)

            # If end is 0 (Present), assume current year (mock 2026 for now)
            # A real system would use datetime objects.
            years_spent = (end if end > 0 else 2026) - (start if start > 0 else 2026)
            if years_spent > 0 and years_spent < 50:
                candidate_years += years_spent
                evidence_texts.append(f"{exp.title.value} ({years_spent} yrs)")

    # Evaluate Match
    match_level = MatchLevel.MISSING
    if candidate_years >= req_years:
        match_level = MatchLevel.EXACT
    elif candidate_years >= req_years - 1 and req_years > 1:
        match_level = MatchLevel.PARTIAL
    elif candidate_years > 0:
        match_level = MatchLevel.WEAK

    return [
        EvidenceResult(
            requirement=jd.experience_requirements.value,
            match_level=match_level,
            evidence_found=", ".join(evidence_texts) if evidence_texts else None,
        )
    ]


def collect_education_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    """Collects evidence for education matching."""
    if jd.education_requirements.verification_state == "Hallucinated":
        return []

    best_match_level = MatchLevel.MISSING
    best_match_text = None

    for edu in resume.education:
        if edu.degree.verification_state != "Hallucinated":
            level = evaluate_similarity(
                edu.degree.value, jd.education_requirements.value
            )
            if level in [MatchLevel.EXACT, MatchLevel.SEMANTIC]:
                best_match_level = level
                best_match_text = edu.degree.value
                break
            elif level == MatchLevel.PARTIAL and best_match_level == MatchLevel.MISSING:
                best_match_level = MatchLevel.PARTIAL
                best_match_text = edu.degree.value

    return [
        EvidenceResult(
            requirement=jd.education_requirements.value,
            match_level=best_match_level,
            evidence_found=best_match_text,
        )
    ]


def collect_title_evidence(
    resume: VerifiedParsedResume, jd: VerifiedJD
) -> List[EvidenceResult]:
    """Collects evidence for title domain matching."""
    if jd.job_title.verification_state == "Hallucinated":
        return []

    best_match_level = MatchLevel.MISSING
    best_match_text = None

    for exp in resume.experience:
        if exp.title.verification_state != "Hallucinated":
            level = evaluate_similarity(exp.title.value, jd.job_title.value)
            if level in [MatchLevel.EXACT, MatchLevel.SEMANTIC]:
                best_match_level = level
                best_match_text = exp.title.value
                break
            elif level == MatchLevel.PARTIAL and best_match_level == MatchLevel.MISSING:
                best_match_level = MatchLevel.PARTIAL
                best_match_text = exp.title.value

    return [
        EvidenceResult(
            requirement=jd.job_title.value,
            match_level=best_match_level,
            evidence_found=best_match_text,
        )
    ]
