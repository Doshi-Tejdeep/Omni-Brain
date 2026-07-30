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
        embedding = self.model.encode(text)
        return embedding.tolist()