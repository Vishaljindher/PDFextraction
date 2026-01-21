import re


def clean_text(text: str) -> str:
    """
    Clean raw extracted text for question parsing.
    """

    if not text or not isinstance(text, str):
        return ""

    text = _normalize_text(text)
    text = _remove_headers_footers(text)
    text = _remove_page_numbers(text)
    text = _remove_noise(text)
    text = _fix_spacing(text)

    return text.strip()


# ------------------ Cleaning Steps ------------------ #

def _normalize_text(text: str) -> str:
    """
    Normalize encoding and line breaks
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")
    return text


def _remove_headers_footers(text: str) -> str:
    """
    Remove repeated headers/footers (simple heuristic)
    """
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line_strip = line.strip()

        # skip very short uppercase lines (headers)
        if line_strip.isupper() and len(line_strip) < 40:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def _remove_page_numbers(text: str) -> str:
    """
    Remove page numbers like:
    Page 1, 1/10, - 2 -
    """
    patterns = [
        r"^\s*page\s*\d+\s*$",
        r"^\s*\d+\s*/\s*\d+\s*$",
        r"^\s*-\s*\d+\s*-\s*$"
    ]

    lines = text.split("\n")
    cleaned = []

    for line in lines:
        skip = False
        for pattern in patterns:
            if re.match(pattern, line.strip().lower()):
                skip = True
                break

        if not skip:
            cleaned.append(line)

    return "\n".join(cleaned)


def _remove_noise(text: str) -> str:
    """
    Remove OCR / extraction noise
    """
    # weird unicode chars
    text = re.sub(r"[�•►■◆]", " ", text)

    # multiple dots or hyphens
    text = re.sub(r"\.{3,}", " ", text)
    text = re.sub(r"-{3,}", " ", text)

    return text


def _fix_spacing(text: str) -> str:
    """
    Fix spacing issues
    """
    # multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # more than 2 line breaks → 2 max
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text
