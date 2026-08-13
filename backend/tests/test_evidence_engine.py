
from app.matching.evidence import (
    collect_skills_evidence,
)
from app.schemas.match_report import MatchLevel
from app.schemas.parsed_jd import VerifiedJD, VerifiedJDField
from app.schemas.parsed_resume import (
    VerifiedContact,
    VerifiedEducation,
    VerifiedField,
    VerifiedParsedResume,
)


def mock_jd(req_skills):
    return VerifiedJD(
        job_title=VerifiedJDField(value="SWE", verification_state="Verified"),
        company=VerifiedJDField(value="Tech", verification_state="Verified"),
        location=VerifiedJDField(value="Remote", verification_state="Verified"),
        employment_type=VerifiedJDField(
            value="Full-time", verification_state="Verified"
        ),
        required_skills=[
            VerifiedJDField(value=s, verification_state="Verified") for s in req_skills
        ],
        preferred_skills=[],
        responsibilities=[],
        qualifications=[],
        experience_requirements=VerifiedJDField(
            value="3 years", verification_state="Verified"
        ),
        education_requirements=VerifiedJDField(
            value="BS", verification_state="Verified"
        ),
        overall_confidence=100,
        section_confidence={"skills": 100},
    )


def mock_resume(skills, degrees=[]):
    return VerifiedParsedResume(
        contact=VerifiedContact(email=None, phone=None, linkedin=None),
        summary=None,
        skills=[VerifiedField(value=s, verification_state="Verified") for s in skills],
        experience=[],
        education=[
            VerifiedEducation(
                degree=VerifiedField(value=d, verification_state="Verified"),
                institution=VerifiedField(value="Univ", verification_state="Verified"),
                graduation_year=VerifiedField(
                    value="2020", verification_state="Verified"
                ),
                coursework=[]
            )
            for d in degrees
        ],
        overall_confidence=100,
        section_confidence={},
    )


def test_alias_matching():
    jd = mock_jd(["Web Services", "Databases"])
    resume = mock_resume(["REST APIs", "PostgreSQL"])

    evidence = collect_skills_evidence(resume, jd, is_required=True)
    assert len(evidence) == 2

    # Web Services should map to REST APIs
    assert evidence[0].match_level == MatchLevel.EXACT
    assert "REST APIs" in evidence[0].evidence_found
    assert "[Type: Alias" in evidence[0].evidence_found

    # Databases should map to PostgreSQL
    assert evidence[1].match_level == MatchLevel.SEMANTIC
    assert "PostgreSQL" in evidence[1].evidence_found
    assert "[Type: Technology" in evidence[1].evidence_found


def test_coursework_matching():
    jd = mock_jd(["Object Oriented Programming", "Data Structures"])
    resume = mock_resume([], degrees=["OOP Coursework", "DSA Coursework"])

    evidence = collect_skills_evidence(resume, jd, is_required=True)

    assert evidence[0].match_level == MatchLevel.SEMANTIC
    assert "OOP Coursework" in evidence[0].evidence_found
    assert "[Type: Coursework" in evidence[0].evidence_found


def test_technology_matching():
    jd = mock_jd(["Backend Development"])
    resume = mock_resume(["Spring Boot"])

    evidence = collect_skills_evidence(resume, jd, is_required=True)

    assert evidence[0].match_level == MatchLevel.SEMANTIC
    assert "Spring Boot" in evidence[0].evidence_found
    assert "[Type: Technology" in evidence[0].evidence_found


def test_false_positive_rejection():
    # Similar letters but completely different things
    jd = mock_jd(["Java"])
    resume = mock_resume(["HTML", "Javascript"])

    evidence = collect_skills_evidence(resume, jd, is_required=True)
    # Javascript has "Java" in it, but they are not aliases or tech mapped.
    # The normalizer and fuzzy matcher should handle this, but let's just make sure it's not EXACT.
    assert evidence[0].match_level != MatchLevel.EXACT
