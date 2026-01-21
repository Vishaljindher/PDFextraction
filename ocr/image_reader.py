import os
import cv2
import numpy as np
import pytesseract

# Explicit tesseract path (Windows fix)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def read_image(image_path: str) -> str:
    """
    Extract text from image using OCR.
    Returns raw extracted text.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = _load_image(image_path)
    processed = _preprocess_image(image)
    text = _extract_text(processed)

    return text


# ------------------ Helpers ------------------ #

def _load_image(path: str):
    """
    Load image using OpenCV
    """
    image = cv2.imread(path)

    if image is None:
        raise ValueError("Unable to load image")

    return image


def _preprocess_image(image):
    """
    Improve image quality for OCR (MCQ / Question papers)
    """

    # 1️⃣ Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2️⃣ Resize (OCR works better on larger text)
    gray = cv2.resize(
        gray, None,
        fx=1.5, fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # 3️⃣ Noise removal
    gray = cv2.medianBlur(gray, 3)

    # 4️⃣ Thresholding (strong text separation)
    thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # 5️⃣ Morphological opening (remove small dots)
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return thresh


def _extract_text(image):
    """
    Run tesseract OCR with tuned config
    """

    config = (
        "--oem 3 "
        "--psm 6 "
        "-l eng "
        "-c preserve_interword_spaces=1"
    )

    text = pytesseract.image_to_string(image, config=config)
    return text
