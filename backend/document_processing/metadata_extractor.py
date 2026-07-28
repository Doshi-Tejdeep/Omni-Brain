"""PDF metadata extraction utilities for OmniBrain."""

from pathlib import Path

import fitz  # PyMuPDF


def extract_metadata_from_pdf(pdf_path: str) -> dict:
    """Extract metadata from a PDF."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with fitz.open(path) as document:
        metadata = document.metadata

        return {
            "title": metadata.get("title"),
            "author": metadata.get("author"),
            "subject": metadata.get("subject"),
            "creator": metadata.get("creator"),
            "producer": metadata.get("producer"),
            "creation_date": metadata.get("creationDate"),
            "modification_date": metadata.get("modDate"),
            "page_count": document.page_count,
        }