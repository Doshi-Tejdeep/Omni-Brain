import io
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from backend.app.main import app

client = TestClient(app)


def create_test_pdf():
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(
        100,
        750,
        "OmniBrain is an Agentic Multi Modal RAG Orchestrator."
    )

    pdf.drawString(
        100,
        730,
        "It uses document processing, embeddings and vector search."
    )

    pdf.save()

    buffer.seek(0)

    return buffer.read()


@patch("backend.document_processing.index_document.get_embeddings")
def test_upload_to_rag_pipeline(mock_get_embeddings):

    mock_model = MagicMock()
    mock_model.embed_query.return_value = [0.0] * 768
    mock_get_embeddings.return_value = mock_model

    pdf_content = create_test_pdf()

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "omnibrain_test.pdf",
                pdf_content,
                "application/pdf"
            )
        }
    )

    assert upload_response.status_code == 200

    ask_response = client.post(
        "/ask",
        json={
            "question": "What is OmniBrain?"
        }
    )

    assert ask_response.status_code == 200

    data = ask_response.json()

    assert "question" in data
    assert "answer" in data

    assert "answer" in data["answer"]
    assert "sources" in data["answer"]

    assert len(data["answer"]["answer"]) > 0
    assert len(data["answer"]["sources"]) > 0
