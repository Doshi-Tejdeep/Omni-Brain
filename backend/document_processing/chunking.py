"""
Document chunking utilities.

Splits extracted document text into smaller chunks for embedding.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits text into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk_text(self, text: str):
        """
        Split text into chunks.
        """
        return self.splitter.split_text(text)


def chunk_pages(
    pages,
    chunk_size: int = 500,
    overlap: int = 50,
):
    """
    Split a list of pages into chunks while preserving page metadata.

    Expected input:
    [
        {"page": 1, "text": "..."},
        {"page": 2, "text": "..."},
    ]

    Returns:
    [
        {"text": "...", "page": 1},
        {"text": "...", "page": 1},
        {"text": "...", "page": 2},
    ]
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    chunks = []

    for page in pages:
        text_chunks = splitter.split_text(page["text"])

        for chunk_text in text_chunks:
            chunks.append(
                {
                    "text": chunk_text,
                    "page": page["page"],
                }
            )

    return chunks
