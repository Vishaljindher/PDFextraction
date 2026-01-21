import os
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd

from ocr.image_reader import read_image


SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".txt", ".png", ".jpg", ".jpeg"]


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


# ------------------ Extractors ------------------ #

def _extract_pdf(path: str) -> str:
    text = []
    reader = PdfReader(path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def _extract_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])


def _extract_excel(path: str) -> str:
    df = pd.read_excel(path, sheet_name=None)
    text = []

    for sheet in df.values():
        text.append(sheet.astype(str).to_string())

    return "\n".join(text)


def _extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_image(path: str) -> str:
    return read_image(path)
