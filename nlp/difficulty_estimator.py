# nlp/difficulty_estimator.py

def estimate_difficulty(question):
    length = len(question.split())

    hard_keywords = ["explain", "analyze", "why", "how", "difference", "describe"]

    if length <= 8:
        return "EASY"

    if any(word in question.lower() for word in hard_keywords):
        return "HARD"

    return "MEDIUM"
