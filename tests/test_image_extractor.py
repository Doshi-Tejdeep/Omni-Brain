from backend.document_processing.image_extractor import (
    extract_images_from_pdf,
)

images = extract_images_from_pdf(
    "sample_data/image_sample.pdf",
    "sample_data/extracted_images",
)

if images:
    print("Images found:")
    for image in images:
        print(image)
else:
    print("No embedded images found in the PDF.")