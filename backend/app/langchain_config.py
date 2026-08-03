from langchain_ollama import ChatOllama
 

def get_llm():
    """Return the configured Ollama LLM."""
    return ChatOllama(
        model="llama3.2",
        temperature=0,
    )
