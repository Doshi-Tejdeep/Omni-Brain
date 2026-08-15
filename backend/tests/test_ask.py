from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.app.main import app

client = TestClient(app)


def test_empty_question():
    response = client.post(
        "/ask",
        json={
            "question": "",
            "document_id": "test-document-id",
        },
    )

    assert response.status_code == 400


@patch("backend.app.routes.ask.generate_answer")
def test_valid_question(mock_generate_answer):
    mock_generate_answer.return_value = {
        "question": "What is OmniBrain?",
        "answer": "OmniBrain is an AI-powered document intelligence system.",
        "sources": [],
    }

    response = client.post(
        "/ask",
        json={
            "question": "What is OmniBrain?",
            "document_id": "test-document-id",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "question" in data
    assert "answer" in data
