import re
from enum import Enum

class MatchLevel(str, Enum):
    EXACT = "Exact"
    SEMANTIC = "Semantic"
    PARTIAL = "Partial"
    WEAK = "Weak"
    MISSING = "Missing"

def evaluate_similarity(source: str, target: str) -> MatchLevel:
    if not source or not target:
        return MatchLevel.MISSING

    s_lower = source.lower().strip()
    t_lower = target.lower().strip()

    # 1. Exact Match
    if s_lower == t_lower:
        return MatchLevel.EXACT

    # 2. Partial Substring Match with Word Boundaries
    boundary_start = r"(?:^|[^\w+#])"
    boundary_end = r"(?:$|[^\w+#])"
    pattern_s = boundary_start + re.escape(s_lower) + boundary_end
    pattern_t = boundary_start + re.escape(t_lower) + boundary_end

    print(f"pattern_s: {pattern_s}")
    print(f"pattern_t: {pattern_t}")
    print(f"search pattern_s in t_lower: {re.search(pattern_s, t_lower)}")
    print(f"search pattern_t in s_lower: {re.search(pattern_t, s_lower)}")

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

s = "B.Tech in Computer Science and Engineering"
t = "Bachelor's degree in Computer Science, Computer Engineering, or a related technical field"

result = evaluate_similarity(s, t)
print(f"Result: {result}")
