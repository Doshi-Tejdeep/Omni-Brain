from pathlib import Path

from backend.document_processing.pdf_parser import extract_text_from_pdf
from backend.document_processing.chunker import chunk_pages
from backend.vector_db.embeddings import get_embeddings
from backend.vector_db.vector_store import VectorStore


def index_document(pdf_path):
    """
    Extract text from a PDF, split it into chunks,
    generate embeddings for each chunk,
    and store them in the vector database.
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        return []

    chunks = chunk_pages(pages)

    embedding_model = get_embeddings()

    for chunk in chunks:
        chunk["embedding"] = embedding_model.embed_query(chunk["text"])

    db = VectorStore()
    db.connect()
    db.add_document(chunks)

    return chunks
