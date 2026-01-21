# nlp/question_classifier.py

def classify_question(text):
    text_lower = text.lower()

    if "a)" in text_lower and "b)" in text_lower:
        return "MCQ"

    if "true" in text_lower or "false" in text_lower:
        return "TRUE_FALSE"

    if len(text.split()) > 25:
        return "LONG_ANSWER"

    return "SHORT_ANSWER"
