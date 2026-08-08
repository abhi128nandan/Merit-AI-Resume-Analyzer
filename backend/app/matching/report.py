from app.matching.policies import MatchingPolicy
from app.schemas.match_report import MatchCategoryResult, MatchReport


def generate_match_report(
    skills_eval: MatchCategoryResult,
    exp_eval: MatchCategoryResult,
    edu_eval: MatchCategoryResult,
    title_eval: MatchCategoryResult,
    policy: MatchingPolicy,
    has_hallucinations: bool,
) -> MatchReport:
    """Generates the final MatchReport by applying category weights."""

    overall_score = int(
        (skills_eval.score * policy.skills_weight)
        + (exp_eval.score * policy.experience_weight)
        + (edu_eval.score * policy.education_weight)
        + (title_eval.score * policy.title_weight)
    )

    return MatchReport(
        overall_score=overall_score,
        skills_evaluation=skills_eval,
        experience_evaluation=exp_eval,
        education_evaluation=edu_eval,
        title_evaluation=title_eval,
        confidence_warning=has_hallucinations,
    )
