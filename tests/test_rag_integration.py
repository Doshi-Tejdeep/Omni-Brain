import io
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from backend.app.main import app

client = TestClient(app)


def create_test_pdf():
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 750, "OmniBrain is an Agentic Multi Modal RAG Orchestrator.")

    pdf.drawString(
        100, 730, "It uses document processing, embeddings and vector search."
    )

    pdf.save()

    buffer.seek(0)

    return buffer.read()


@patch("backend.app.services.rag_service.get_llm")
@patch("backend.app.services.rag_service.VectorStore.search")
@patch("backend.document_processing.index_document.get_embeddings")
def test_upload_to_rag_pipeline(
    mock_get_embeddings,
    mock_search,
    mock_get_llm,
):
    # Mock embeddings
    embedding_model = MagicMock()
    embedding_model.embed_query.return_value = [0.0] * 768
    mock_get_embeddings.return_value = embedding_model

    # Mock vector search
    mock_search.return_value = [
        {
            "text": "OmniBrain is an Agentic Multi Modal RAG Orchestrator.",
            "page_number": "1",
            "chunk_id": "0",
        }
    ]

    # Mock LLM
    llm = MagicMock()

    response = MagicMock()
    response.content = "OmniBrain is an Agentic Multi Modal RAG Orchestrator."

    llm.invoke.return_value = response
    mock_get_llm.return_value = llm

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "omnibrain_test.pdf",
                pdf_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200
    upload_data = upload_response.json()
    document_id = upload_data["document_id"]

    ask_response = client.post(
        "/ask",
        json={
            "question": "What is OmniBrain?",
            "document_id": document_id,
        },
    )

    assert ask_response.status_code == 200
    

    data = ask_response.json()

    assert "question" in data
    assert "answer" in data
    assert "sources" in data

    assert data["answer"] == "OmniBrain is an Agentic Multi Modal RAG Orchestrator."
    assert "Page 1" in data["sources"]

    assert len(data["answer"]) > 0
