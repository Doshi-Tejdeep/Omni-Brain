"""PDF text extraction utilities for OmniBrain."""

from pathlib import Path

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from a PDF page by page."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_pages = []

    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                extracted_pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                    }
                )

    return extracted_pages