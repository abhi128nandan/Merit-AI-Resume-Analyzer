from app.matching.evidence import collect_experience_evidence
from app.matching.policies import DEFAULT_POLICY
from app.matching.scorer import calculate_evidence_score
from app.matching.similarity import evaluate_similarity
from app.schemas.match_report import EvidenceResult, MatchLevel
from app.schemas.parsed_jd import VerifiedJD, VerifiedJDField
from app.schemas.parsed_resume import (
    VerifiedContact,
    VerifiedEducation,
    VerifiedExperience,
    VerifiedField,
    VerifiedParsedResume,
)

from app.matching.normalizer import EducationNormalizer
from app.matching.evidence import collect_education_evidence

def test_education_normalizer():
    # Test level extraction and specialization extraction
    lvl, spec = EducationNormalizer.parse("B.Tech in Computer Science and Engineering")
    assert lvl == "Bachelor"
    assert "computer science" in spec

    lvl, spec = EducationNormalizer.parse("Bachelor's degree in Computer Science, Computer Engineering, or a related technical field")
    assert lvl == "Bachelor"
    assert "computer science" in spec
    assert "computer engineering" in spec

    lvl, spec = EducationNormalizer.parse("Master of Science in Data Science")
    assert lvl == "Master"
    assert "data science" in spec

    lvl, spec = EducationNormalizer.parse("Ph.D in Machine Learning")
    assert lvl == "Doctorate"
    assert "machine learning" in spec

def test_education_matching():
    # Create mock resume and JD
    resume = build_mock_verified_resume()
    jd = build_mock_verified_jd()
    
    # 1. Test semantic match (B.Tech in CS vs Bachelor's in CS)
    resume.education = [
        VerifiedEducation(
            degree=VerifiedField(value="B.Tech in Computer Science and Engineering", verification_state="Verified"),
            institution=VerifiedField(value="Univ", verification_state="Verified"),
            graduation_year=VerifiedField(value="2020", verification_state="Verified"),
            coursework=[]
        )
    ]
    jd.education_requirements = VerifiedJDField(value="Bachelor's degree in Computer Science", verification_state="Verified")
    evidence = collect_education_evidence(resume, jd)
    assert evidence[0].match_level == MatchLevel.SEMANTIC
    
    # 2. Test negative match (Bachelor of Arts in English vs Bachelor's in CS)
    resume.education = [
        VerifiedEducation(
            degree=VerifiedField(value="Bachelor of Arts in English", verification_state="Verified"),
            institution=VerifiedField(value="Univ", verification_state="Verified"),
            graduation_year=VerifiedField(value="2020", verification_state="Verified"),
            coursework=[]
        )
    ]
    evidence = collect_education_evidence(resume, jd)
    assert evidence[0].match_level == MatchLevel.MISSING
    
    # 3. Test Master satisfies Bachelor requirement
    resume.education = [
        VerifiedEducation(
            degree=VerifiedField(value="Master of Science in Computer Science", verification_state="Verified"),
            institution=VerifiedField(value="Univ", verification_state="Verified"),
            graduation_year=VerifiedField(value="2020", verification_state="Verified"),
            coursework=[]
        )
    ]
    evidence = collect_education_evidence(resume, jd)
    assert evidence[0].match_level == MatchLevel.SEMANTIC

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


from app.matching.report import generate_match_report
from app.schemas.match_report import MatchCategoryResult

def test_generate_match_report_all_categories():
    policy = DEFAULT_POLICY
    skills_eval = MatchCategoryResult(score=80, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    exp_eval = MatchCategoryResult(score=90, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    edu_eval = MatchCategoryResult(score=100, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    title_eval = MatchCategoryResult(score=70, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])

    report = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    
    # 80*0.4 + 90*0.3 + 100*0.15 + 70*0.15 = 32 + 27 + 15 + 10.5 = 84.5 -> int(84)
    assert report.overall_score == 84
    assert skills_eval.applied_weight == 0.40
    assert exp_eval.applied_weight == 0.30
    assert edu_eval.applied_weight == 0.15
    assert title_eval.applied_weight == 0.15

def test_generate_match_report_education_missing():
    policy = DEFAULT_POLICY
    skills_eval = MatchCategoryResult(score=80, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    exp_eval = MatchCategoryResult(score=90, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    edu_eval = MatchCategoryResult(score=0, evidence=[])
    title_eval = MatchCategoryResult(score=70, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])

    report = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    
    # Weights sum = 0.4 + 0.3 + 0.15 = 0.85
    # Score = (80*0.4 + 90*0.3 + 70*0.15) / 0.85 = (32 + 27 + 10.5) / 0.85 = 69.5 / 0.85 = 81.76 -> 81
    assert report.overall_score == 81
    assert edu_eval.applied_weight == 0.0

def test_generate_match_report_title_missing():
    policy = DEFAULT_POLICY
    skills_eval = MatchCategoryResult(score=80, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    exp_eval = MatchCategoryResult(score=90, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    edu_eval = MatchCategoryResult(score=100, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    title_eval = MatchCategoryResult(score=0, evidence=[])

    report = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    
    # Weights sum = 0.4 + 0.3 + 0.15 = 0.85
    # Score = (80*0.4 + 90*0.3 + 100*0.15) / 0.85 = (32 + 27 + 15) / 0.85 = 74 / 0.85 = 87.05 -> 87
    assert report.overall_score == 87
    assert title_eval.applied_weight == 0.0

def test_generate_match_report_multiple_missing():
    policy = DEFAULT_POLICY
    skills_eval = MatchCategoryResult(score=80, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    exp_eval = MatchCategoryResult(score=0, evidence=[])
    edu_eval = MatchCategoryResult(score=0, evidence=[])
    title_eval = MatchCategoryResult(score=0, evidence=[])

    report = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    assert report.overall_score == 80  # 100% weight to skills
    assert skills_eval.applied_weight == 0.40

def test_determinism_exact_same_input():
    policy = DEFAULT_POLICY
    skills_eval = MatchCategoryResult(score=80, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    exp_eval = MatchCategoryResult(score=90, evidence=[EvidenceResult(requirement="Req", match_level=MatchLevel.EXACT, evidence_found="x")])
    edu_eval = MatchCategoryResult(score=100, evidence=[])
    title_eval = MatchCategoryResult(score=70, evidence=[])

    report1 = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    report2 = generate_match_report(skills_eval, exp_eval, edu_eval, title_eval, policy, False)
    assert report1.overall_score == report2.overall_score

def test_weight_sum_valid():
    policy = DEFAULT_POLICY
    policy.validate_weights()
    
def test_boundary_scores():
    policy = DEFAULT_POLICY
    # All 0
    s_0 = MatchCategoryResult(score=0, evidence=[EvidenceResult(requirement="R", match_level=MatchLevel.MISSING, evidence_found="")])
    report_0 = generate_match_report(s_0, s_0, s_0, s_0, policy, False)
    assert report_0.overall_score == 0
    
    # All 100
    s_100 = MatchCategoryResult(score=100, evidence=[EvidenceResult(requirement="R", match_level=MatchLevel.EXACT, evidence_found="")])
    report_100 = generate_match_report(s_100, s_100, s_100, s_100, policy, False)
    assert report_100.overall_score == 100
    
    # No evidence at all
    s_empty = MatchCategoryResult(score=0, evidence=[])
    report_empty = generate_match_report(s_empty, s_empty, s_empty, s_empty, policy, False)
    assert report_empty.overall_score == 0
