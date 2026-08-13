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

    # 2. Partial Substring Match with Word Boundaries
    # We shouldn't match 'sql' in 'nosql' or 'c' in 'c++'.
    # Only match if it's a distinct word boundary. Treating + and # as word chars.
    boundary_start = r"(?:^|[^\w+#])"
    boundary_end = r"(?:$|[^\w+#])"
    pattern_s = boundary_start + re.escape(s_lower) + boundary_end
    pattern_t = boundary_start + re.escape(t_lower) + boundary_end

    if re.search(pattern_s, t_lower) or re.search(pattern_t, s_lower):
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
        if any(w == s_lower for w in syn_set) and any(w == t_lower for w in syn_set):
            return MatchLevel.SEMANTIC

    return MatchLevel.MISSING


MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def extract_months_of_experience(
    exp_string: str, is_date: bool = False, is_end: bool = False
) -> int:
    """Extracts duration in months from a string."""
    if not exp_string:
        return 0

    exp_string = exp_string.lower().strip()

    if not is_date:
        # Extracting "3 years", "6 months", "3-5 years"
        # We'll just take the first number. If it says months, use it. Else assume years.
        matches = re.findall(r"\d+", exp_string)
        if matches:
            val = int(matches[0])
            if "month" in exp_string:
                return val
            return val * 12
        return 0

    # It's a date like "Jan 2023", "2023", "Present"
    if "present" in exp_string or "current" in exp_string:
        return 2026 * 12 + 8  # Hardcoded to Aug 2026 for now based on system time

    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", exp_string)
    if not year_match:
        return 0

    year = int(year_match.group(1))

    # Try to find month
    month = 12 if is_end else 1
    for m_name, m_val in MONTH_MAP.items():
        if re.search(r"\b" + m_name + r"\b", exp_string):
            month = m_val
            break

    return year * 12 + month
