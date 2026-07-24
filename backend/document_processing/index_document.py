from backend.document_processing.pdf_parser import extract_text_from_pdf
from backend.document_processing.chunker import chunk_document
from backend.vector_db.embeddings import get_embeddings

def index_document(pdf_path):
    """
    Extract text from a PDF, split it into chunks,
    generate embeddings for each chunk,
    and return the embedded chunks.
    """

    pages = extract_text_from_pdf(pdf_path)

    chunks = chunk_document(pages)

    embedding_model = get_embeddings()

    for chunk in chunks:
        chunk["embedding"] = embedding_model.embed_query(chunk["text"])

    return chunks