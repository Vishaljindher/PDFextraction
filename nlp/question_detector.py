import re

QUESTION_WORDS = [
    "what", "why", "how", "when", "where", "who", "whom", "which",
    "define", "explain", "describe", "discuss", "write",
    "differentiate", "compare", "list", "state", "give reason",
    "short note",
    "kya", "kyon", "kaise"
]


def detect_questions(text: str):
    """
    Detect question blocks WITHOUT breaking MCQs
    """

    if not text or not isinstance(text, str):
        return []

    text = _normalize_text(text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    questions = []
    current_q = []

    for line in lines:
        if is_question_start(line):
            if current_q:
                questions.append("\n".join(current_q))
                current_q = []
            current_q.append(line)
        else:
            if current_q:
                current_q.append(line)

    if current_q:
        questions.append("\n".join(current_q))

    return [
        q for q in questions
        if is_valid_question(q)
    ]


# ---------------- CORE LOGIC ---------------- #

def is_question_start(line: str) -> bool:
    """
    STRICT question start detector
    (MCQ options are explicitly blocked)
    """

    if not line or len(line) < 6:
        return False

    line_strip = line.strip()

    # ❌ MCQ options must NEVER start a question
    if re.match(r"^[A-Da-d][\)\.]\s+", line_strip):
        return False

    # Q1. Q2) Ql. (OCR safe)
    if re.match(r"^(q[\d]+[\.\)])", line_strip.lower()):
        return True

    # 1. 2)
    if re.match(r"^\d+[\.\)]\s+", line_strip):
        return True

    # Question mark ONLY if it looks like a sentence
    if line_strip.endswith("?") and len(line_strip.split()) > 3:
        return True

    # Question words
    if _starts_with_question_word(line_strip):
        return True

    return False


def is_valid_question(text: str) -> bool:
    """
    Filters section headers / instructions
    """

    if len(text) < 15:
        return False

    blacklist = [
        "section", "true / false", "choose one",
        "short answer", "instructions"
    ]

    t = text.lower()
    return not any(b in t for b in blacklist)


# ---------------- HELPERS ---------------- #

def _starts_with_question_word(text: str) -> bool:
    text = text.lower()
    for word in QUESTION_WORDS:
        if text.startswith(word + " "):
            return True
    return False


def _normalize_text(text: str) -> str:
    """
    OCR normalization WITHOUT destroying MCQ structure
    """

    replacements = {
        "qi.": "q1.",
        "ql.": "q1.",
        "qa": "q4",
        "©)": "C)",
        "8)": "B)",
        "0)": "D)"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # preserve case, just fix spacing
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text
