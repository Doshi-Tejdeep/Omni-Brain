"""Table extraction utilities for OmniBrain."""

from pathlib import Path

import fitz  # PyMuPDF


def extract_tables_from_pdf(pdf_path: str) -> list[dict]:
    """Extract tables from a PDF page by page."""

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_tables = []

    with fitz.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            tables = page.find_tables()

            for index, table in enumerate(tables.tables, start=1):
                extracted_tables.append(
                    {
                        "page_number": page_number,
                        "table_number": index,
                        "data": table.extract(),
                    }
                )

    return extracted_tables