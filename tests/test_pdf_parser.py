import pytest

from backend.document_processing.pdf_parser import extract_text_from_pdf


def test_pdf_not_found():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("sample_data/file_does_not_exist.pdf")


def test_extract_text():
    pages = extract_text_from_pdf("sample_data/sample.pdf")

    assert isinstance(pages, list)