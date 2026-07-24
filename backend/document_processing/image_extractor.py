"""Image extraction utilities for OmniBrain."""

from pathlib import Path

import fitz  # PyMuPDF


def extract_images_from_pdf(pdf_path: str, output_dir: str) -> list[dict]:
    """Extract images from a PDF and save them."""

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    extracted_images = []

    with fitz.open(pdf_file) as document:
        for page_number, page in enumerate(document, start=1):
            images = page.get_images(full=True)

            for image_number, image in enumerate(images, start=1):
                xref = image[0]
                image_data = document.extract_image(xref)

                image_bytes = image_data["image"]
                extension = image_data["ext"]

                filename = (
                    f"page_{page_number}_image_{image_number}.{extension}"
                )

                image_path = output_path / filename

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                extracted_images.append(
                    {
                        "page_number": page_number,
                        "image_number": image_number,
                        "filename": filename,
                        "path": str(image_path),
                    }
                )

    return extracted_images