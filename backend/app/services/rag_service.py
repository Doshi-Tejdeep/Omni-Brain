from backend.vector_db.vector_store import VectorStore
from backend.app.langchain_config import get_llm
from backend.app.prompts import SEARCH_PROMPT
import traceback


async def generate_answer(
    question: str,
    document_id: str,
):
    """
    Executes the complete RAG pipeline:
    1. Search ChromaDB
    2. Build context
    3. Generate answer using Ollama
    4. Return answer + sources
    """

    try:
        print("\n==============================")
        print("Starting RAG Pipeline")
        print("==============================")

        print(f"Question: {question}")

        # -------------------------------
        # Vector Store
        # -------------------------------
        print("\n1. Connecting to Vector Store...")
        vector_store = VectorStore()

        print("2. Searching ChromaDB...")
        chunks = vector_store.search(
            question,
            k=8,
            document_id=document_id,
        )

        print(f"Retrieved {len(chunks)} chunks")

        print("\n========== Retrieved Pages ==========\n")

        for i, chunk in enumerate(chunks, start=1):
            print(f"Rank {i}")
            print(f"Page: {chunk['page_number']}")
            print(f"Chunk: {chunk['chunk_id']}")
            print("-" * 40)

        if not chunks:
            print("No chunks found.")
            return {
                "answer": "I could not find the answer in the provided documents.",
                "sources": [],
            }

        # -------------------------------
        # Context
        # -------------------------------
        print("\n3. Building Context...")

        context = "\n\n".join(chunk["text"] for chunk in chunks)

        print("\n========== Context ==========\n")
        print(context)

        # -------------------------------
        # Prompt
        # -------------------------------
        print("\n4. Formatting Prompt...")

        prompt = SEARCH_PROMPT.format(
            context=context,
            question=question,
        )

        print("Prompt formatted successfully.")

        # -------------------------------
        # Load LLM
        # -------------------------------
        print("\n5. Loading Ollama LLM...")

        llm = get_llm()

        print("LLM loaded successfully.")

        # -------------------------------
        # Invoke LLM
        # -------------------------------
        print("\n6. Calling LLM...")

        response = llm.invoke(prompt)

        print("LLM call completed.")

        print("\n========== Raw Response ==========")
        print(response)

        answer = response.content if hasattr(response, "content") else str(response)

        # -------------------------------
        # Sources
        # -------------------------------
        sources = list(
            dict.fromkeys([f"Page {chunk['page_number']}" for chunk in chunks])
        )

        print("\nSources:", sources)

        print("\nRAG Pipeline Completed Successfully.")

        return {
            "answer": answer,
            "sources": sources,
        }

    except Exception as e:
        print("\n===================================")
        print("RAG PIPELINE FAILED")
        print("===================================")
        traceback.print_exc()
        print("\nException:", e)
        raise
