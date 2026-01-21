import re

QUESTION_WORDS = [
    "what", "why", "how", "when", "where", "who", "whom", "which",
    "define", "explain", "describe", "discuss", "write", "differentiate",
    "compare", "list", "state", "give reason", "short note",
    "kya", "kyon", "kaise"   # Hinglish support
]


def detect_questions(text: str):
    """
    Detects question blocks from OCR text.
    Works well for MCQ, True/False, Short Answer papers.
    """

    if not text or not isinstance(text, str):
        return []

    # -------- Normalize OCR noise -------- #
    text = _normalize_text(text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    questions = []

    current_q = []

    for line in lines:
        if is_question_start(line):
            if current_q:
                questions.append(" ".join(current_q))
                current_q = []
            current_q.append(line)
        else:
            if current_q:
                current_q.append(line)

    if current_q:
        questions.append(" ".join(current_q))

    # Final cleanup
    questions = [
        q.strip() for q in questions
        if is_valid_question(q)
    ]

    return questions


# ------------------ Core Logic ------------------ #

def is_question_start(line: str) -> bool:
    """
    Strong question start detector (OCR tolerant)
    """

    if len(line) < 8:
        return False

    # Q1. Q2) QA Ql (OCR mistakes)
    if re.match(r"^(q[\dla]+[\.\)])", line.lower()):
        return True

    # 1. 2) 3.
    if re.match(r"^\d+[\.\)]", line):
        return True

    # Question mark
    if "?" in line:
        return True

    # Question words
    if _starts_with_question_word(line):
        return True

    return False


def is_valid_question(text: str) -> bool:
    """
    Filters garbage OCR lines
    """

    if len(text) < 20:
        return False

    blacklist = [
        "section", "true / false", "choose one",
        "short answer", "instructions"
    ]

    t = text.lower()
    for b in blacklist:
        if b in t:
            return False

    return True


# ------------------ Helpers ------------------ #

def _starts_with_question_word(text: str) -> bool:
    text = text.lower()
    for word in QUESTION_WORDS:
        if text.startswith(word + " "):
            return True
    return False


def _normalize_text(text: str) -> str:
    """
    Fix common OCR mistakes
    """

    replacements = {
        "qi.": "q1.",
        "ql.": "q1.",
        "qa": "q4",
        "0)": "D)",
        "©)": "C)",
        "8)": "B)",
        "a)": "A)",
        "b)": "B)",
        "c)": "C)",
        "d)": "D)"
    }

    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Remove excessive spaces
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)

    return text
