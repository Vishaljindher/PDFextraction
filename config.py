# config.py

SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt", ".xlsx", ".png", ".jpg"]

OCR_LANGUAGE = "eng+hin"

# Regex patterns
QUESTION_REGEX = r"(Q\d+[\.\)]|^\d+[\.\)])"
OPTION_REGEX = r"^[A-D][\)\.]"
ANSWER_REGEX = r"Answer\s*:\s*[A-D]|True|False"

# NLP thresholds
QUESTION_CONFIDENCE_THRESHOLD = 0.6
