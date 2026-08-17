from backend.vector_db.vector_store import VectorStore
from backend.app.langchain_config import get_llm
from backend.app.prompts import SEARCH_PROMPT
from backend.app.utils.logger import logger


async def generate_answer(
    question: str,
    document_id: str,
):
    """
    Executes the complete RAG pipeline:
    1. Search ChromaDB for chunks belonging to the selected document
    2. Build context
    3. Generate answer using Ollama
    4. Return answer + sources
    """

    logger.info(f"Generating answer for: {question}")
    logger.info(f"Using document_id: {document_id}")

    vector_store = VectorStore()

    chunks = vector_store.search(
        question,
        k=8,
        document_id=document_id,
    )

    logger.info(
        f"Retrieved {len(chunks)} chunks for document {document_id}"
    )

    if not chunks:
        return {
            "answer": "I could not find the answer in the provided documents.",
            "sources": [],
        }

    context = "\n\n".join(
        chunk["text"] for chunk in chunks
    )

    prompt = SEARCH_PROMPT.format(
        context=context,
        question=question,
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    sources = list(
        dict.fromkeys(
            f"Page {chunk['page_number']}"
            for chunk in chunks
        )
    )

    logger.info(f"Retrieved sources: {sources}")

    return {
        "answer": answer,
        "sources": sources,
    }
