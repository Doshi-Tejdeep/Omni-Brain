from langchain_ollama import ChatOllama


def get_llm():
    """
    Returns the configured Ollama LLM.
    """

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    return llm
