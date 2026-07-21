from backend.document_processing.chunker import chunk_text, chunk_pages


def test_chunk_text():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=500, overlap=50)

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