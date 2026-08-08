import re
import unicodedata


def clean_extracted_text(text: str) -> str:
    """Normalizes and cleans extracted text for downstream LLM processing.

    This function performs the following deterministic operations:
    1. Normalizes Unicode characters (NFKC) to resolve ligatures (e.g., 'ﬁ' -> 'fi').
    2. Removes non-printable or hidden control characters.
    3. Normalizes line endings to a single '\n'.
    4. Collapses multiple contiguous spaces or tabs into a single space.
    5. Normalizes various bullet points to a standard '-'.
    6. Strips leading/trailing whitespace.

    Args:
        text: The raw text extracted from the document.

    Returns:
        The pristine, cleaned text string.
    """
    if not text:
        return ""

    # 1. Normalize Unicode (NFKC handles compatibility characters and ligatures)
    text = unicodedata.normalize("NFKC", text)

    # 2. Remove non-printable characters (keep newline and tab)
    # \x00-\x08, \x0B-\x0C, \x0E-\x1F, \x7F
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # 3. Normalize line endings (\r\n -> \n, \r -> \n)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 4. Normalize bullet points (•, ▪, ◦, ‣, ⁃, etc. to '-')
    text = re.sub(r"[•▪◦‣⁃\u2022\u2023\u25E6\u2043\u2219]", "-", text)

    # 5. Collapse multiple spaces/tabs within a line (but preserve newlines)
    # We split by line, replace spaces, and join back.
    cleaned_lines = []
    for line in text.split("\n"):
        # Replace multiple spaces with a single space
        cleaned_line = re.sub(r"[ \t]+", " ", line).strip()
        # Only add lines that have content (removes multiple empty newlines)
        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    # Join with a single newline
    text = "\n".join(cleaned_lines)

    return text.strip()
