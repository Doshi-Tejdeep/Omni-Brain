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

        print(
            f"Vector store connected. "
            f"Current chunks: {self.vector_db._collection.count()}"
        )

        self.connected = True

    def add_document(self, document, document_id=None):
        """
        Store document chunks and their embeddings in ChromaDB.

        Each chunk receives a document_id so different uploaded
        documents can be separated during retrieval.
        """

        if not self.connected:
            self.connect()

        if not document:
            return

        document_id = document_id or str(uuid.uuid4())

        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for chunk in document:
            chunk_id = str(uuid.uuid4())

            ids.append(chunk_id)
            texts.append(chunk["text"])
            embeddings.append(chunk["embedding"])

            metadatas.append(
                {
                    "document_id": document_id,
                    "page_number": str(chunk.get("page_number") or "unknown"),
                    "chunk_id": str(chunk.get("chunk_id", 0)),
                }
            )

        self.vector_db._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"Stored {len(ids)} chunks successfully " f"for document {document_id}.")

    def search(self, query, k=4, document_id=None):
        """
        Retrieve the most relevant chunks from ChromaDB.

        If document_id is supplied, only chunks belonging to that
        document are retrieved.
        """

        if not self.connected:
            self.connect()

        filter_metadata = None

        if document_id:
            filter_metadata = {"document_id": document_id}

        results = self.vector_db.similarity_search_with_score(
            query=query.strip(),
            k=k,
            filter=filter_metadata,
        )

        chunks = []
        seen = set()

        for doc, score in results:
            page_number = doc.metadata.get(
                "page_number",
                "unknown",
            )

            chunk_id = doc.metadata.get(
                "chunk_id",
                "unknown",
            )

            document_id_value = doc.metadata.get(
                "document_id",
                "unknown",
            )

            # Prevent duplicate chunks from entering the context.
            unique_key = (
                document_id_value,
                page_number,
                chunk_id,
            )

            if unique_key in seen:
                continue

            seen.add(unique_key)

            print(f"\nPage: {page_number}")
            print(f"Chunk: {chunk_id}")
            print(f"Document: {document_id_value}")
            print(f"Score: {score}")

            chunks.append(
                {
                    "text": doc.page_content,
                    "page_number": page_number,
                    "chunk_id": chunk_id,
                    "document_id": document_id_value,
                }
            )

        return chunks

    def delete_document(self, document_id):
        """
        Delete all embeddings belonging to a document.
        """

        if not self.connected:
            self.connect()

        self.vector_db._collection.delete(where={"document_id": document_id})

        print(f"Deleted document embeddings: {document_id}")
