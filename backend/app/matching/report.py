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

    active_weight_sum = 0.0
    weighted_score = 0.0

    if skills_eval.evidence:
        active_weight_sum += policy.skills_weight
        weighted_score += skills_eval.score * policy.skills_weight

    if exp_eval.evidence:
        active_weight_sum += policy.experience_weight
        weighted_score += exp_eval.score * policy.experience_weight

    if edu_eval.evidence:
        active_weight_sum += policy.education_weight
        weighted_score += edu_eval.score * policy.education_weight

    if title_eval.evidence:
        active_weight_sum += policy.title_weight
        weighted_score += title_eval.score * policy.title_weight

    if active_weight_sum > 0:
        overall_score = int(weighted_score / active_weight_sum)
    else:
        overall_score = 0

    return MatchReport(
        overall_score=overall_score,
        skills_evaluation=skills_eval,
        experience_evaluation=exp_eval,
        education_evaluation=edu_eval,
        title_evaluation=title_eval,
        confidence_warning=has_hallucinations,
    )
