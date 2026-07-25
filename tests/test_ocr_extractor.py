from backend.document_processing.ocr_extractor import (
    extract_text_with_ocr,
)

def test_extract_text_with_ocr():
    pages = extract_text_with_ocr("sample_data/sample.pdf")

    assert pages is not None
    assert isinstance(pages, list)
    