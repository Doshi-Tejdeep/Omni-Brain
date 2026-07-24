from langchain_ollama import OllamaEmbeddings


def get_embeddings():
    """
    Returns the embedding model used
    throughout the RAG pipeline.
    """

    return OllamaEmbeddings(
        model="nomic-embed-text"
    )