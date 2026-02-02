import re


def clean_text(text: str) -> str:
    """
    Clean raw extracted text for question parsing
    (MCQ / Exam friendly)
    """

    if not text or not isinstance(text, str):
        return ""

    text = _normalize_text(text)
    text = _remove_headers_footers(text)
    text = _remove_page_numbers(text)
    text = _remove_noise(text)
    text = _fix_spacing_safe(text)

    return text.strip()


# ================= CLEANING STEPS ================= #

def _normalize_text(text: str) -> str:
    """
    Normalize encoding and line breaks
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")
    return text


def _remove_headers_footers(text: str) -> str:
    """
    Remove obvious headers / footers without killing content
    """
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line_strip = line.strip()

        # skip empty
        if not line_strip:
            cleaned.append(line)
            continue

        # skip very short ALL CAPS lines with NO digits (true headers)
        if (
            line_strip.isupper()
            and len(line_strip) < 30
            and not re.search(r"\d", line_strip)
        ):
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
        if any(re.match(p, line.strip().lower()) for p in patterns):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def _remove_noise(text: str) -> str:
    """
    Remove OCR / extraction noise (SAFE)
    """
    # remove weird unicode chars only
    text = re.sub(r"[�•►■◆]", " ", text)

    # remove long dot / hyphen runs ONLY
    text = re.sub(r"\.{4,}", " ", text)
    text = re.sub(r"-{4,}", " ", text)

    return text


def _fix_spacing_safe(text: str) -> str:
    """
    Fix spacing WITHOUT destroying MCQ structure
    """
    # collapse multiple spaces (but keep newlines)
    text = re.sub(r"[ \t]{2,}", " ", text)

    # normalize excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # ensure space after option markers
    text = re.sub(r"([A-D][\)\.])([^\s])", r"\1 \2", text)

    return text
