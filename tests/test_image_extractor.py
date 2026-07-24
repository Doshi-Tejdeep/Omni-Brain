from backend.document_processing.image_extractor import (
    extract_images_from_pdf,
)

def test_extract_images():
    images = extract_images_from_pdf(
        "sample_data/image_sample.pdf",
        "sample_data/extracted_images",
    )

    assert images is not None
    assert isinstance(images, list)