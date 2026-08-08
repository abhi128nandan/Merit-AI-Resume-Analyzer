import re

from app.schemas.match_report import MatchLevel


def evaluate_similarity(source: str, target: str) -> MatchLevel:
    """Evaluates the semantic similarity between two strings and returns a MatchLevel.

    Args:
        source: A string from the candidate's resume (e.g. "AWS").
        target: A requirement from the JD (e.g. "Amazon Web Services").

    Returns:
        MatchLevel: EXACT, SEMANTIC, PARTIAL, WEAK, or MISSING.
    """
    if not source or not target:
        return MatchLevel.MISSING

    s_lower = source.lower().strip()
    t_lower = target.lower().strip()

    # 1. Exact Match
    if s_lower == t_lower:
        return MatchLevel.EXACT

    # 2. Partial Substring Match
    if s_lower in t_lower or t_lower in s_lower:
        # Check if it's a very weak substring (like 'c' in 'c++')
        if len(s_lower) <= 2 and s_lower != t_lower:
            return MatchLevel.WEAK
        return MatchLevel.PARTIAL

    # 3. Semantic / Synonym Matching
    synonyms = [
        {"aws", "amazon web services"},
        {"gcp", "google cloud platform"},
        {"azure", "microsoft azure"},
        {"js", "javascript", "node.js", "nodejs"},
        {"backend", "back end", "back-end", "server-side"},
        {"frontend", "front end", "front-end", "client-side", "ui", "user interface"},
        {"ml", "machine learning", "ai", "artificial intelligence"},
        {"bachelor", "b.s.", "bs", "bachelors", "undergraduate"},
        {"master", "m.s.", "ms", "masters", "graduate"},
    ]

    for syn_set in synonyms:
        if any(w in s_lower for w in syn_set) and any(w in t_lower for w in syn_set):
            return MatchLevel.SEMANTIC

    return MatchLevel.MISSING


def extract_years_of_experience(exp_string: str) -> int:
    """Extracts numeric years of experience from a string."""
    if not exp_string:
        return 0
    matches = re.findall(r"\d+", exp_string)
    if matches:
        return int(matches[0])
    return 0
