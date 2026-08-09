from app.matching.evidence import collect_experience_evidence
from app.matching.policies import DEFAULT_POLICY
from app.matching.scorer import calculate_evidence_score
from app.matching.similarity import evaluate_similarity
from app.schemas.match_report import EvidenceResult, MatchLevel
from app.schemas.parsed_jd import VerifiedJD, VerifiedJDField
from app.schemas.parsed_resume import (
    VerifiedContact,
    VerifiedExperience,
    VerifiedField,
    VerifiedParsedResume,
)


def test_similarity_exact_match():
    assert evaluate_similarity("Python", "Python") == MatchLevel.EXACT
    assert evaluate_similarity(" python ", "PYTHON") == MatchLevel.EXACT


def test_similarity_partial_match():
    assert evaluate_similarity("C++", "C++ 14") == MatchLevel.PARTIAL
    assert (
        evaluate_similarity("Machine Learning", "Machine Learning Engineer")
        == MatchLevel.PARTIAL
    )


def test_similarity_semantic_match():
    assert evaluate_similarity("AWS", "Amazon Web Services") == MatchLevel.SEMANTIC
    assert evaluate_similarity("NodeJS", "JavaScript") == MatchLevel.SEMANTIC


def test_similarity_weak_match():
    assert evaluate_similarity("c", "c++") == MatchLevel.MISSING
    assert evaluate_similarity("go", "google cloud platform") == MatchLevel.MISSING


def test_similarity_missing_match():
    assert evaluate_similarity("Python", "Java") == MatchLevel.MISSING
    assert evaluate_similarity("", "Java") == MatchLevel.MISSING


def test_calculate_evidence_score():
    evidence = [
        EvidenceResult(
            requirement="Req 1", match_level=MatchLevel.EXACT, evidence_found="Req 1"
        ),
        EvidenceResult(
            requirement="Req 2", match_level=MatchLevel.MISSING, evidence_found=None
        ),
    ]

    # EXACT = 1.0, MISSING = 0.0 -> total earned = 1.0. total max = 2.0 -> 50%
    score = calculate_evidence_score(evidence, DEFAULT_POLICY)
    assert score == 50


def build_mock_verified_resume() -> VerifiedParsedResume:
    return VerifiedParsedResume(
        contact=VerifiedContact(email=None, phone=None, linkedin=None),
        summary=None,
        skills=[
            VerifiedField(value="Python", verification_state="Verified"),
            VerifiedField(value="AWS", verification_state="Verified"),
            # Hallucinated skill that should be ignored
            VerifiedField(value="Docker", verification_state="Hallucinated"),
        ],
        experience=[
            VerifiedExperience(
                title=VerifiedField(
                    value="Senior Engineer", verification_state="Verified"
                ),
                company=VerifiedField(value="Tech Inc", verification_state="Verified"),
                start_date=VerifiedField(value="2020", verification_state="Verified"),
                end_date=VerifiedField(value="2023", verification_state="Verified"),
                responsibilities=[],
            )
        ],
        education=[],
        overall_confidence=100,
        section_confidence={},
    )


def build_mock_verified_jd() -> VerifiedJD:
    return VerifiedJD(
        job_title=VerifiedJDField(
            value="Senior Backend Engineer", verification_state="Verified"
        ),
        company=VerifiedJDField(value="Startup", verification_state="Verified"),
        location=VerifiedJDField(value="Remote", verification_state="Verified"),
        employment_type=VerifiedJDField(
            value="Full-time", verification_state="Verified"
        ),
        required_skills=[
            VerifiedJDField(value="Python", verification_state="Verified"),
            VerifiedJDField(value="Docker", verification_state="Verified"),
        ],
        preferred_skills=[
            VerifiedJDField(value="AWS", verification_state="Verified"),
        ],
        responsibilities=[],
        qualifications=[],
        experience_requirements=VerifiedJDField(
            value="3+ years", verification_state="Verified"
        ),
        education_requirements=VerifiedJDField(
            value="B.S.", verification_state="Verified"
        ),
        overall_confidence=100,
        section_confidence={},
    )


def test_experience_evidence_collection():
    resume = build_mock_verified_resume()
    jd = build_mock_verified_jd()

    # Resume has 2023 - 2020 = 3 years
    # JD requires 3+ years
    evidence = collect_experience_evidence(resume, jd)
    assert len(evidence) == 1
    assert evidence[0].match_level == MatchLevel.EXACT
    assert "Senior Engineer (3.9 yrs)" in evidence[0].evidence_found
