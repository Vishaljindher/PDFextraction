# utils/regex_patterns.py

QUESTION_NUMBER = r"(Q\d+[\.\)]|\d+[\.\)])"
MCQ_OPTION = r"[A-D][\)\.]"
ANSWER = r"Answer\s*:\s*[A-D]|True|False"
