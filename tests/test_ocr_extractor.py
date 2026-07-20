from backend.document_processing.ocr_extractor import (
    extract_text_with_ocr,
)

pages = extract_text_with_ocr("sample_data/sample.pdf")

for page in pages:
    print(f"Page {page['page_number']}")
    print(page["text"])
    print("-" * 40)