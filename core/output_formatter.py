# core/output_formatter.py
import uuid
from datetime import datetime


def format_output(
    question: str,
    q_type: str = "unknown",
    difficulty: str = "unknown",
    source: str = "unknown",
    options: dict | None = None,
    answer: str | None = None
) -> dict:
    """
    Format a question into a clean, production-ready structure.
    """

    return {
        "id": _generate_id(),
        "question": _clean_text(question),
        "type": q_type,
        "difficulty": difficulty,
        "options": options or {},
        "answer": answer,
        "source": source,
        "meta": {
            "length": len(question.split()),
            "created_at": _timestamp(),
            "version": "1.0"
        }
    }


# ------------------ Helpers ------------------ #

def _generate_id() -> str:
    return str(uuid.uuid4())


def _timestamp() -> str:
    return datetime.utcnow().isoformat()


def _clean_text(text: str) -> str:
    """
    Final cleanup before saving
    """
    return " ".join(text.strip().split())
