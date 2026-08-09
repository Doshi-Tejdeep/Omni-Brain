from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_empty_question():
    response = client.post("/ask", json={"question": ""})

    assert response.status_code == 400


def test_valid_question():
    response = client.post("/ask", json={"question": "What is OmniBrain?"})

    assert response.status_code == 200

    data = response.json()

    assert "question" in data
    assert "answer" in data
