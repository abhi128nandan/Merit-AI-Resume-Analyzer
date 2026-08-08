import re
from typing import Sequence


from app.schemas.parsed_resume import (
    LLMExtractedResume,
    VerifiedContact,
    VerifiedEducation,
    VerifiedExperience,
    VerifiedField,
    VerifiedParsedResume,
)


def verify_field(
    extracted_value: str | None, original_text: str
) -> VerifiedField | None:
    """Verifies a single extracted string against the original cleaned text.

    Verification rules:
    - If None or empty, returns None.
    - Verified: Exact substring match (case-insensitive).
    - Partially Verified: All significant words (>3 chars) found somewhere in the text.
    - Hallucinated: No significant words found in the text.

    Args:
        extracted_value: The string extracted by the LLM.
        original_text: The original cleaned text.

    Returns:
        VerifiedField instance with state.
    """
    if not extracted_value or not str(extracted_value).strip():
        return None

    extracted_str = str(extracted_value).strip()
    original_lower = original_text.lower()
    extracted_lower = extracted_str.lower()

    # 1. Exact Match
    if extracted_lower in original_lower:
        return VerifiedField(value=extracted_str, verification_state="Verified")

    # 2. Partial Match (Check words > 3 chars)
    words = [w for w in re.findall(r"\b\w+\b", extracted_lower) if len(w) > 3]
    if not words:
        # If no significant words and not an exact match, assume Unverified
        return VerifiedField(value=extracted_str, verification_state="Unverified")

    matched_words = sum(1 for word in words if word in original_lower)

    if matched_words == len(words):
        # All significant words exist, but not in that exact phrase order
        return VerifiedField(
            value=extracted_str, verification_state="Partially Verified"
        )
    elif matched_words > 0:
        return VerifiedField(value=extracted_str, verification_state="Unverified")
    else:
        # None of the significant words exist
        return VerifiedField(value=extracted_str, verification_state="Hallucinated")


def verify_resume_data(
    llm_resume: LLMExtractedResume, original_text: str
) -> VerifiedParsedResume:
    """Verifies an entire LLM-extracted resume against the original text.

    Returns a VerifiedParsedResume, which also calculates confidence scores.
    """

    # Verify Contact
    v_contact = VerifiedContact(
        email=verify_field(llm_resume.contact.email, original_text),
        phone=verify_field(llm_resume.contact.phone, original_text),
        linkedin=verify_field(llm_resume.contact.linkedin, original_text),
    )

    # Verify Summary
    v_summary = verify_field(llm_resume.summary, original_text)

    # Verify Skills
    v_skills = []
    for skill in llm_resume.skills:
        vf = verify_field(skill, original_text)
        if vf:
            v_skills.append(vf)

    # Verify Experience
    v_experience = []
    for exp in llm_resume.experience:
        v_exp = VerifiedExperience(
            title=verify_field(exp.title, original_text)
            or VerifiedField(value=exp.title, verification_state="Unverified"),
            company=verify_field(exp.company, original_text)
            or VerifiedField(value=exp.company, verification_state="Unverified"),
            start_date=verify_field(exp.start_date, original_text)
            or VerifiedField(value=exp.start_date, verification_state="Unverified"),
            end_date=verify_field(exp.end_date, original_text)
            or VerifiedField(value=exp.end_date, verification_state="Unverified"),
            responsibilities=[
                verify_field(r, original_text)
                or VerifiedField(value=r, verification_state="Unverified")
                for r in exp.responsibilities
            ],
        )
        v_experience.append(v_exp)

    # Verify Education
    v_education = []
    for edu in llm_resume.education:
        v_edu = VerifiedEducation(
            degree=verify_field(edu.degree, original_text)
            or VerifiedField(value=edu.degree, verification_state="Unverified"),
            institution=verify_field(edu.institution, original_text)
            or VerifiedField(value=edu.institution, verification_state="Unverified"),
            graduation_year=verify_field(edu.graduation_year, original_text)
            or VerifiedField(
                value=edu.graduation_year, verification_state="Unverified"
            ),
        )
        v_education.append(v_edu)

    # Calculate Section Confidences
    def calculate_section_confidence(
        verified_fields: Sequence[VerifiedField | None],
    ) -> int:
        fields = [f for f in verified_fields if f is not None]
        if not fields:
            return 0
        score = 0
        for f in fields:
            if f.verification_state == "Verified":
                score += 100
            elif f.verification_state == "Partially Verified":
                score += 70
            elif f.verification_state == "Unverified":
                score += 30
            elif f.verification_state == "Hallucinated":
                score += 0
        return int(score / len(fields))

    # Flatten fields for confidence calculation
    contact_fields = [v_contact.email, v_contact.phone, v_contact.linkedin]
    exp_fields = []
    for e in v_experience:
        exp_fields.extend(
            [e.title, e.company, e.start_date, e.end_date] + e.responsibilities
        )
    edu_fields = []
    for v_ed in v_education:
        edu_fields.extend([v_ed.degree, v_ed.institution, v_ed.graduation_year])

    section_confidence = {
        "contact": calculate_section_confidence(contact_fields),
        "summary": calculate_section_confidence([v_summary]) if v_summary else 0,
        "skills": calculate_section_confidence(v_skills),
        "experience": calculate_section_confidence(exp_fields),
        "education": calculate_section_confidence(edu_fields),
    }

    # Calculate Overall Confidence
    weights = {
        "contact": 0.1,
        "summary": 0.05,
        "skills": 0.2,
        "experience": 0.5,
        "education": 0.15,
    }
    overall_confidence = int(sum(section_confidence[k] * weights[k] for k in weights))

    return VerifiedParsedResume(
        contact=v_contact,
        summary=v_summary,
        skills=v_skills,
        experience=v_experience,
        education=v_education,
        overall_confidence=overall_confidence,
        section_confidence=section_confidence,
    )
