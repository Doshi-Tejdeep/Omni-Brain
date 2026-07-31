"""
Embedding generation utilities.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates vector embeddings from text.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str):
        """
        Convert text into a vector embedding.
        """
        return self.model.encode(text).tolist()

    def embed_query(self, text: str):
        """
        Generate embedding for a search query.
        """
        return self.model.encode(text).tolist()

    def embed_documents(self, texts):
        """
        Generate embeddings for multiple documents.
        """
        return [self.model.encode(text).tolist() for text in texts]


def get_embeddings():
    """
    Return the embedding generator instance.
    """
    return EmbeddingGenerator()