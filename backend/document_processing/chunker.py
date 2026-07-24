"""Text chunking utilities for OmniBrain."""

from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[str]:
    """Split text into overlapping chunks."""

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_pages(
    pages: List[Dict],
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Dict]:
    """Chunk extracted PDF pages while preserving page metadata."""

    chunked_pages = []

    for page in pages:
        text = page.get("text", "")
        chunks = chunk_text(text, chunk_size, overlap)

        for index, chunk in enumerate(chunks):
            chunked_pages.append(
                {
                    "page": page.get("page"),
                    "chunk_index": index,
                    "text": chunk,
                }
            )

    return chunked_pages
