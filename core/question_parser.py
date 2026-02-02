import re
from nlp.question_detector import is_question_start


# ================= MAIN ================= #

def extract_questions(text: str):
    if not text or not isinstance(text, str):
        return []

    lines = _split_lines(text)

    questions = []
    current_block = []

    for line in lines:
        if is_question_start(line):
            if current_block:
                q = _format_question(current_block)
                if q:
                    questions.append(q)
                current_block = []
            current_block.append(line)
        else:
            if current_block:
                current_block.append(line)

    if current_block:
        q = _format_question(current_block)
        if q:
            questions.append(q)

    return questions


# ================= HELPERS ================= #

def _split_lines(text: str):
    text = text.replace("\r", "\n")
    return [l.strip() for l in text.split("\n") if l.strip()]


def _format_question(lines: list):
    block = " ".join(lines)
    block = _remove_section_noise(block)
    block = _clean_numbering(block)

    question_text = _extract_question_text(block)
    options = _extract_options(block)
    answer = _extract_answer(block)

    if not question_text:
        return None

    # Detect type
    if options:
        q_type = "MCQ"
    elif re.search(r"\b(true|false)\b", block, re.I):
        q_type = "TRUE_FALSE"
    else:
        q_type = "SHORT"

    return {
        "question": question_text,
        "options": options,
        "answer": answer,
        "type": q_type,
        "length": len(question_text.split())
    }


# ================= CLEANERS ================= #

def _remove_section_noise(text: str):
    # Remove section headers, emojis, labels
    noise_patterns = [
        r"SECTION\s+[A-Z].*",
        r"True\s*/\s*False",
        r"📗|📙|📕|📘",
    ]
    for p in noise_patterns:
        text = re.sub(p, "", text, flags=re.I)

    return text.strip()


def _clean_numbering(text: str):
    patterns = [
        r"^Q[\dA-Za-z]+[\.\)]\s*",
        r"^\d+[\.\)]\s*",
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.I)
    return text.strip()


# ================= EXTRACTION ================= #

def _extract_question_text(block: str):
    # Remove Answer part
    block = re.split(r"Answer\s*:", block, flags=re.I)[0]

    # Stop before first option
    split = re.split(r"\bA[\)\.]\s*", block, maxsplit=1)
    return split[0].strip()


def _extract_options(block: str):
    options = {}

    # Handle both inline & multiline OCR
    matches = re.findall(
        r"([A-D])[\)\.]\s*(.*?)(?=[A-D][\)\.]|Answer\s*:|$)",
        block,
        re.I
    )

    for key, value in matches:
        clean_val = value.strip(" :-")
        if clean_val:
            options[key.upper()] = clean_val

    return options


def _extract_answer(block: str):
    # MCQ / TF answers
    match = re.search(
        r"Answer\s*:\s*(?:Option\s*)?([A-D]|True|False)",
        block,
        re.I
    )
    if match:
        return match.group(1).upper()

    return None
