from typing import List

from app.matching.policies import MatchingPolicy
from app.schemas.match_report import EvidenceResult, MatchCategoryResult, MatchLevel


def calculate_evidence_score(
    evidence_list: List[EvidenceResult], policy: MatchingPolicy
) -> int:
    """Calculates a normalized score (0-100) from a list of evidence based on the policy."""
    if not evidence_list:
        return 0

    total_max = len(evidence_list) * policy.score_exact
    if total_max == 0:
        return 0

    total_earned = 0.0
    for ev in evidence_list:
        if ev.match_level == MatchLevel.EXACT:
            total_earned += policy.score_exact
        elif ev.match_level == MatchLevel.SEMANTIC:
            total_earned += policy.score_semantic
        elif ev.match_level == MatchLevel.PARTIAL:
            total_earned += policy.score_partial
        elif ev.match_level == MatchLevel.WEAK:
            total_earned += policy.score_weak
        elif ev.match_level == MatchLevel.MISSING:
            total_earned += policy.score_missing
        elif ev.match_level == MatchLevel.HALLUCINATED:
            total_earned += policy.score_hallucinated

    return int((total_earned / total_max) * 100)


def score_skills(
    req_evidence: List[EvidenceResult],
    pref_evidence: List[EvidenceResult],
    policy: MatchingPolicy,
) -> MatchCategoryResult:
    """Scores skills based on required/preferred weights in the policy."""

    req_score = calculate_evidence_score(req_evidence, policy)
    pref_score = calculate_evidence_score(pref_evidence, policy)

    # If there are no preferred skills, required skills count for 100% of the skills score
    if not pref_evidence:
        final_score = req_score
    elif not req_evidence:
        final_score = pref_score
    else:
        final_score = int(
            (req_score * policy.required_skills_weight)
            + (pref_score * policy.preferred_skills_weight)
        )

    combined_evidence = req_evidence + pref_evidence

    return MatchCategoryResult(score=final_score, evidence=combined_evidence)


def score_category(
    evidence_list: List[EvidenceResult], policy: MatchingPolicy
) -> MatchCategoryResult:
    """Generic category scorer."""
    score = calculate_evidence_score(evidence_list, policy)
    return MatchCategoryResult(score=score, evidence=evidence_list)
