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