import pytest

from backend.document_processing.chunker import (
    chunk_text,
    chunk_pages,
)


def test_chunk_text_empty():
    """Test that empty text returns an empty list."""
    assert chunk_text("") == []


def test_chunk_text_single_chunk():
    """Test chunking when text fits in one chunk."""
    text = "Hello OmniBrain!"
    chunks = chunk_text(text, chunk_size=100)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_multiple_chunks():
    """Test chunking of longer text."""
    text = "A" * 1000
    chunks = chunk_text(
        text,
        chunk_size=500,
        overlap=50,
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 500


def test_invalid_overlap():
    """Test that invalid overlap raises ValueError."""
    with pytest.raises(
        ValueError,
        match="overlap must be smaller than chunk_size",
    ):
        chunk_text(
            "Hello OmniBrain",
            chunk_size=100,
            overlap=100,
        )


def test_chunk_pages():
    """Test chunking while preserving page metadata."""
    pages = [
        {
            "page": 1,
            "text": "A" * 600,
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=500,
        overlap=50,
    )

    assert len(chunks) == 2
    assert chunks[0]["page"] == 1
    assert chunks[0]["chunk_index"] == 0
    assert "text" in chunks[0]

    assert chunks[1]["page"] == 1
    assert chunks[1]["chunk_index"] == 1
    assert "text" in chunks[1]