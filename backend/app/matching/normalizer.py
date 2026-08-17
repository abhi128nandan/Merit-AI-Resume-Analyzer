import re

# Deterministic dictionary for domain-specific singularization
# Avoid generic rules that can corrupt unrelated words (e.g. 'express' -> 'expres')
SINGULARIZATION_DICT = {
    "databases": "database",
    "services": "service",
    "technologies": "technology",
    "apis": "api",
    "systems": "system",
    "structures": "structure"
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
    term = re.sub(r'[-_]', ' ', term)
    # Remove punctuation (everything except alphanumeric and whitespace)
    # Note: we want to keep '+' and '#' for C++ and C#
    term = re.sub(r'[^\w\s+#]', '', term)
    # Normalize whitespace to single space
    term = re.sub(r'\s+', ' ', term)
    
    return term.strip()
