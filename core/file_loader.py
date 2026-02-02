import os
import re
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd

from ocr.image_reader import read_image


SUPPORTED_EXTENSIONS = [
    ".pdf", ".docx", ".xlsx", ".txt", ".png", ".jpg", ".jpeg"
]


def load_file(file_path: str) -> str:
    """
    Detect file type and extract raw text.
    Returns extracted text as string.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        return _extract_pdf(file_path)

    elif ext == ".docx":
        return _extract_docx(file_path)

    elif ext == ".xlsx":
        return _extract_excel(file_path)

    elif ext == ".txt":
        return _extract_txt(file_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        return _extract_image(file_path)

    return ""


# ================= EXTRACTORS ================= #

def _extract_pdf(path: str) -> str:
    """
    Extract text from PDF and make MCQ structure parser-friendly
    """
    text_blocks = []
    reader = PdfReader(path)

    for page in reader.pages:
        page_text = page.extract_text()
        if not page_text:
            continue

        # Force newlines before MCQ options & Answer
        page_text = _normalize_mcq_structure(page_text)
        text_blocks.append(page_text)

    return "\n".join(text_blocks)


def _extract_docx(path: str) -> str:
    """
    Extract text from DOCX while preserving MCQ structure
    """
    doc = Document(path)
    lines = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        text = _normalize_mcq_structure(text)
        lines.append(text)

    return "\n".join(lines)


def _extract_excel(path: str) -> str:
    """
    Extract text from Excel (basic support)
    """
    df = pd.read_excel(path, sheet_name=None)
    text = []

    for sheet in df.values():
        text.append(sheet.astype(str).to_string())

    return "\n".join(text)


def _extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_image(path: str) -> str:
    """
    OCR image text and normalize MCQ structure
    """
    text = read_image(path)
    return _normalize_mcq_structure(text)


# ================= HELPERS ================= #

def _normalize_mcq_structure(text: str) -> str:
    """
    Make MCQ options & answers appear on separate lines
    """

    # Newline before options A) B) C) D)
    text = re.sub(r"([ \t])([A-D][\)\.])", r"\n\2", text)

    # Newline before Answer:
    text = re.sub(r"(Answer\s*:)", r"\n\1", text, flags=re.I)

    return text
