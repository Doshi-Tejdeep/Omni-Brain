from vector_db.vector_store import VectorStore
from app.langchain_config import get_llm
from app.prompts import SEARCH_PROMPT
from app.utils.logger import logger


async def generate_answer(question: str):
    """
    Executes the complete RAG pipeline:
    1. Search ChromaDB
    2. Build context
    3. Generate answer using Ollama
    4. Return answer + sources
    """

    logger.info(f"Generating answer for: {question}")

    vector_store = VectorStore()

    # Retrieve relevant chunks
    chunks = vector_store.search(question, k=4)

    if not chunks:
        return {
            "answer": "I could not find the answer in the provided documents.",
            "sources": []
        }

    # Build context
    context = "\n\n".join(chunk["text"] for chunk in chunks)

    # Build prompt
    prompt = SEARCH_PROMPT.format(
        context=context,
        question=question
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    sources = [
        f"Page {chunk['page_number']}"
        for chunk in chunks
    ]

    # Remove duplicate page numbers
    sources = list(dict.fromkeys(sources))

    return {
        "answer": answer,
        "sources": sources
    }