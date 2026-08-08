"""Render PDF pages as images for the Vision Agent."""

from pathlib import Path
import fitz


def render_pdf_page(
    pdf_path: str,
    page_number: int,
    output_dir: str = "uploads/rendered_pages",
) -> str:
    """
    Render a PDF page as a PNG image.

    page_number is 1-based.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with fitz.open(pdf_path) as document:

        if page_number < 1 or page_number > len(document):
            raise ValueError(
                f"Invalid page number: {page_number}. "
                f"PDF contains {len(document)} pages."
            )

        page = document[page_number - 1]

        # Increase resolution for better chart reading
        matrix = fitz.Matrix(2, 2)

        pixmap = page.get_pixmap(matrix=matrix, alpha=False)

        output_path = (
            output_dir / f"page_{page_number}.png"
        )

        pixmap.save(str(output_path))

    return str(output_path)