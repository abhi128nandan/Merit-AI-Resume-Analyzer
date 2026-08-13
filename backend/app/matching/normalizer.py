import re

# Deterministic dictionary for domain-specific singularization
# Avoid generic rules that can corrupt unrelated words (e.g. 'express' -> 'expres')
SINGULARIZATION_DICT = {
    "databases": "database",
    "services": "service",
    "technologies": "technology",
    "apis": "api",
    "systems": "system",
    "structures": "structure",
}


def normalize_term(term: str) -> str:
    """
    Normalizes a term for deterministic matching.
    - Lowercases
    - Replaces hyphens with spaces
    - Trims whitespace
    - Removes punctuation
    - Normalizes internal whitespace
    - Singularizes based on a strict dictionary
    """
    if not term:
        return ""

    term = term.lower().strip()

    # Apply deterministic singularization early, if the whole term is exactly in the dict
    if term in SINGULARIZATION_DICT:
        term = SINGULARIZATION_DICT[term]

    # Also handle singularization of individual words in a phrase
    words = term.split()
    normalized_words = [SINGULARIZATION_DICT.get(w, w) for w in words]
    term = " ".join(normalized_words)

    # Replace hyphens and underscores with spaces so 'object-oriented' becomes 'object oriented'
    term = re.sub(r"[-_]", " ", term)
    # Remove punctuation (everything except alphanumeric and whitespace)
    # Note: we want to keep '+' and '#' for C++ and C#
    term = re.sub(r"[^\w\s+#]", "", term)
    # Normalize whitespace to single space
    term = re.sub(r"\s+", " ", term)

    return term.strip()


class EducationNormalizer:
    """Normalizes and extracts structured data from raw education strings."""

    LEVEL_MAP = {
        "phd": "Doctorate",
        "ph.d": "Doctorate",
        "doctorate": "Doctorate",
        "master": "Master",
        "m.s": "Master",
        "ms": "Master",
        "msc": "Master",
        "m.tech": "Master",
        "mtech": "Master",
        "mba": "Master",
        "bachelor": "Bachelor",
        "b.s": "Bachelor",
        "bs": "Bachelor",
        "bsc": "Bachelor",
        "b.tech": "Bachelor",
        "btech": "Bachelor",
        "b.e": "Bachelor",
        "undergraduate": "Bachelor",
        "associate": "Associate",
        "high school": "High School",
        "class xii": "High School",
    }

    @classmethod
    def parse(cls, text: str) -> tuple[str, str]:
        """
        Parses a degree string into (level, specialization).
        Returns ("Unknown", normalized_text) if level is not found.
        """
        if not text:
            return "Unknown", ""

        t_lower = text.lower()
        found_level = "Unknown"

        # Sort keys by length descending to match longest first (e.g., "high school" before "school")
        sorted_keys = sorted(cls.LEVEL_MAP.keys(), key=len, reverse=True)

        for key in sorted_keys:
            if re.search(rf"\b{re.escape(key)}\b", t_lower):
                found_level = cls.LEVEL_MAP[key]
                break

        # Extract specialization by stripping out levels and fluff words
        spec = t_lower
        for key in sorted_keys:
            spec = re.sub(rf"\b{re.escape(key)}\b", " ", spec)

        spec = re.sub(r"'s\b", " ", spec)
        spec = re.sub(r"\b(degree|in|of|or|a|related|technical|field)\b", " ", spec)
        spec = re.sub(r"[^\w\s]", " ", spec)
        spec = re.sub(r"\s+", " ", spec).strip()

        return found_level, spec
