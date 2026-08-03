from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_file_type():
    response = client.post(
        "/upload",
        files={
            "file": (
                "sample.txt",
                b"Hello World",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400


def test_empty_pdf():
    response = client.post(
        "/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf"
            )
        }
    )

    assert response.status_code == 400


def test_valid_pdf():
    pdf_content = b"%PDF-1.4\nTest PDF"

    response = client.post(
        "/upload",
        files={
            "file": (
                "sample.pdf",
                pdf_content,
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200
