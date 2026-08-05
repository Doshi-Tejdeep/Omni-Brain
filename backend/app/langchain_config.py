import os
from langchain_ollama import ChatOllama


def get_llm():
    """Return the configured Ollama LLM."""
    return ChatOllama(
        model="llama3.2",
        temperature=0,
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    )
