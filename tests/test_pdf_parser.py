import pytest

from backend.document_processing.pdf_parser import extract_text_from_pdf


def test_pdf_not_found():
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("sample_data/file_does_not_exist.pdf")


def test_extract_text():
    pages = extract_text_from_pdf("sample_data/sample.pdf")

    assert isinstance(pages, list)
    assert len(pages) > 0
    assert "page_number" in pages[0]
    assert "text" in pages[0]
    assert isinstance(pages[0]["page_number"], int)
    assert isinstance(pages[0]["text"], str)


def test_non_pdf_file(tmp_path):
    text_file = tmp_path / "sample.txt"
    text_file.write_text("Hello, OmniBrain!")

    with pytest.raises(ValueError, match="Only PDF files are supported."):
        extract_text_from_pdf(str(text_file))