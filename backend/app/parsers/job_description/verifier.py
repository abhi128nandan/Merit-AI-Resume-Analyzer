from app.parsers.resume.verifier import verify_field
from app.schemas.parsed_jd import LLMExtractedJD, VerifiedJD, VerifiedJDField


def verify_jd_data(llm_jd: LLMExtractedJD, original_text: str) -> VerifiedJD:
    """Verifies an entire LLM-extracted JD against the original text.

    Returns a VerifiedJD, calculating confidence scores.
    """

    def verify(val: str) -> VerifiedJDField:
        vf = verify_field(val, original_text)
        if vf:
            return VerifiedJDField(
                value=vf.value, verification_state=vf.verification_state
            )
        return VerifiedJDField(value=val, verification_state="Unverified")

    v_job_title = verify(llm_jd.job_title)
    v_company = verify(llm_jd.company)
    v_location = verify(llm_jd.location)
    v_employment_type = verify(llm_jd.employment_type)

    v_required_skills = [verify(s) for s in llm_jd.required_skills]
    v_preferred_skills = [verify(s) for s in llm_jd.preferred_skills]
    v_responsibilities = [verify(r) for r in llm_jd.responsibilities]
    v_qualifications = [verify(q) for q in llm_jd.qualifications]

    v_experience = verify(llm_jd.experience_requirements)
    v_education = verify(llm_jd.education_requirements)

    # Calculate Section Confidences
    def calculate_section_confidence(verified_fields: list[VerifiedJDField]) -> int:
        if not verified_fields:
            return 0
        score = 0
        for f in verified_fields:
            if f.verification_state == "Verified":
                score += 100
            elif f.verification_state == "Partially Verified":
                score += 70
            elif f.verification_state == "Unverified":
                score += 30
            elif f.verification_state == "Hallucinated":
                score += 0
        return int(score / len(verified_fields))

    section_confidence = {
        "job_title": calculate_section_confidence([v_job_title]),
        "required_skills": calculate_section_confidence(v_required_skills),
        "preferred_skills": calculate_section_confidence(v_preferred_skills),
        "responsibilities": calculate_section_confidence(v_responsibilities),
        "experience": calculate_section_confidence([v_experience]),
    }

    # Calculate Overall Confidence
    weights = {
        "job_title": 0.20,
        "required_skills": 0.30,
        "preferred_skills": 0.10,
        "responsibilities": 0.20,
        "experience": 0.20,
    }
    overall_confidence = int(sum(section_confidence[k] * weights[k] for k in weights))

    return VerifiedJD(
        job_title=v_job_title,
        company=v_company,
        location=v_location,
        employment_type=v_employment_type,
        required_skills=v_required_skills,
        preferred_skills=v_preferred_skills,
        responsibilities=v_responsibilities,
        qualifications=v_qualifications,
        experience_requirements=v_experience,
        education_requirements=v_education,
        overall_confidence=overall_confidence,
        section_confidence=section_confidence,
    )
