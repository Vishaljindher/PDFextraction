import re
from nlp.question_detector import is_question_start


def extract_questions(text: str):
    """
    Extract question blocks from cleaned text.
    Returns list of dictionaries.
    """

    if not text or not isinstance(text, str):
        return []

    lines = _split_lines(text)

    questions = []
    current_question = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # If line starts a question
        if is_question_start(line):
            if current_question:
                questions.append(_format_question(current_question))
                current_question = ""

            current_question = line

        else:
            # continuation of previous question
            if current_question:
                current_question += " " + line

    if current_question:
        questions.append(_format_question(current_question))

    return questions


# ------------------ Helpers ------------------ #

def _split_lines(text: str):
    text = text.replace("\r", "\n")
    return [l.strip() for l in text.split("\n") if l.strip()]


def _format_question(question_text: str):
    question_text = _clean_numbering(question_text)

    return {
        "question": question_text.strip(),
        "length": len(question_text),
        "type": "unknown"
    }


def _clean_numbering(text: str):
    patterns = [
        r"^Q[\dA-Za-z]+[\.\)]\s*",
        r"^\d+[\.\)]\s*",
        r"^\([a-zA-Z]\)\s*"
    ]

    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.I)

    return text
