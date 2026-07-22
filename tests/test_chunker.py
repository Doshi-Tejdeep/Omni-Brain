import pytest

from backend.document_processing.chunker import chunk_text, chunk_pages


def test_chunk_text():
    text = "Hello " * 200

    chunks = chunk_text(text)

    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunk_pages():
    pages = [
        {
            "page_number": 1,
            "text": "A" * 1000,
        }
    ]

    result = chunk_pages(pages)

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["page_number"] == 1


def test_invalid_overlap():
    with pytest.raises(ValueError, match="overlap must be smaller than chunk_size"):
        chunk_text(
            "Hello OmniBrain",
            chunk_size=100,
            overlap=100,
        )