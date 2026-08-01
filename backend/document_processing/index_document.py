from document_processing.pdf_parser import extract_text_from_pdf
from document_processing.chunker import chunk_pages
from vector_db.embeddings import get_embeddings
from vector_db.vector_store import VectorStore


def index_document(pdf_path):
    """
    Extract text from a PDF, split it into chunks,
    generate embeddings for each chunk,
    and store them in ChromaDB.
    """

    pages = extract_text_from_pdf(pdf_path)

    chunks = chunk_pages(pages)

    embedding_model = get_embeddings()

    for chunk in chunks:
        chunk["embedding"] = embedding_model.embed_query(chunk["text"])

    db = VectorStore()
    db.connect()
    db.add_document(chunks)

    return chunks