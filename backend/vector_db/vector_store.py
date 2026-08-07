"""
Vector Store Integration

Persistent ChromaDB implementation for Omni-Brain.
"""

import uuid

from langchain_chroma import Chroma

from .embeddings import get_embeddings
from .config import (
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
            metadatas.append(
                {
                    "page_number": str(chunk.get("page_number", "unknown")),
                    "chunk_id": str(chunk.get("chunk_id", chunk.get("chunk_index", 0))),
                }
            )

        # Access the underlying Chroma collection
        self.vector_db._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"Stored {len(ids)} chunks successfully.")

    def search(self, query, k=4):
        """
        Retrieve the most relevant chunks from ChromaDB.
        """

        if not self.connected:
            self.connect()

        results = self.vector_db.similarity_search(
            query=query.strip(),
            k=k,
        )

        chunks = []

        for doc in results:
            chunks.append(
                {
                    "text": doc.page_content,
                    "page_number": doc.metadata["page_number"],
                    "chunk_id": doc.metadata["chunk_id"],
                }
            )

        return chunks

    def delete_document(self, document_id):
        """
        Delete document embeddings.
        """
        raise NotImplementedError("Vector DB delete_document() not implemented yet.")
