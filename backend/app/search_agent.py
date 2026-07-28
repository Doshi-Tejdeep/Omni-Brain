from backend.app.state import AgentState
from backend.app.langchain_config import get_llm

from backend.vector_db.vector_store import VectorStore
from backend.app.prompt_builder import build_search_prompt


def search_agent(state: AgentState) -> AgentState:
    """
    Search Agent

    Handles user queries using Retrieval-Augmented Generation (RAG).
    """

    print("Search Agent Executed")

    # Connect to vector database
    db = VectorStore()
    db.connect()

    # Retrieve relevant chunks
    chunks = db.search(state["query"])

    # Build RAG prompt
    prompt = build_search_prompt(
        chunks,
        state["query"]
    )

    # Generate response
    llm = get_llm()
    response = llm.invoke(prompt)

    state["response"] = response.content

    return state