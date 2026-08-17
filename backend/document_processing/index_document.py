from pathlib import Path

from backend.document_processing.pdf_parser import extract_text_from_pdf
from backend.document_processing.chunker import chunk_pages
from backend.vector_db.embeddings import get_embeddings
from backend.vector_db.vector_store import VectorStore


def index_document(pdf_path, document_id):
    """
    Extract text from a PDF, split it into chunks,
    generate embeddings for each chunk,
    and store them in the vector database.

    Args:
        pdf_path: Path to the PDF file.
        document_id: Unique ID assigned to the uploaded document.

    Returns:
        The document_id associated with the indexed document.
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        return None

    chunks = chunk_pages(pages)

    embedding_model = get_embeddings()

    for chunk in chunks:
        chunk["embedding"] = embedding_model.embed_query(chunk["text"])

    db = VectorStore()
    db.connect()
    db.add_document(chunks, document_id=document_id)

    return document_id