"""
Vector Store Integration

Persistent ChromaDB implementation for Omni-Brain.
"""

import uuid

from langchain_chroma import Chroma

from backend.vector_db.embeddings import get_embeddings
from backend.vector_db.config import (
    COLLECTION_NAME,
    CHROMA_DB_PATH,
)


class VectorStore:
    def __init__(self):
        self.connected = False
        self.vector_db = None
        self.embedding_model = get_embeddings()

    def connect(self):
        """
        Initialize persistent ChromaDB connection.
        """

        self.vector_db = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embedding_model,
            persist_directory=CHROMA_DB_PATH,
        )

        self.connected = True

    def add_document(self, document):
        """
        Store document chunks and their embeddings in ChromaDB.
        """

        if not self.connected:
            self.connect()

        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for chunk in document:
            ids.append(str(uuid.uuid4()))
            texts.append(chunk["text"])
            embeddings.append(chunk["embedding"])
            metadatas.append({
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"]
            })

        # Access the underlying Chroma collection
        self.vector_db._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"Stored {len(ids)} chunks successfully.")

    def search(self, query):
        """
        Perform similarity search.
        """
        raise NotImplementedError(
            "Vector DB search() not implemented yet."
        )

    def delete_document(self, document_id):
        """
        Delete document embeddings.
        """
        raise NotImplementedError(
            "Vector DB delete_document() not implemented yet."
        )