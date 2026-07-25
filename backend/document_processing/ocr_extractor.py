"""OCR utilities for OmniBrain."""

from pathlib import Path

import fitz
import pytesseract
from PIL import Image


def extract_text_with_ocr(pdf_path: str) -> list[dict]:
    """Extract text from a PDF using OCR."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_pages = []

    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            pix = page.get_pixmap(dpi=300)

            image = Image.frombytes(
                "RGB",
                (pix.width, pix.height),
                pix.samples,
            )

            text = pytesseract.image_to_string(image)

            extracted_pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    return extracted_pages