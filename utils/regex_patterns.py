# utils/regex_patterns.py

# Question numbering like:
# Q1. , Q2) , 1. , 2)
QUESTION_NUMBER = r"(?:Q\s*\d+|\d+)[\.\)]"

# MCQ options like:
# A) , B. , a) , e.
MCQ_OPTION = r"[A-Ea-e][\)\.]"

# Answer patterns like:
# Answer: A
# ANSWER : TRUE
# Answer: false
ANSWER = r"Answer\s*:\s*(?:[A-Ea-e]|True|False)"
