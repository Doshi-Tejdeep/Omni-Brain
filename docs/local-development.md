# Local Development Guide

## Prerequisites

Before running OmniBrain locally, ensure you have:

- Python 3.12+
- Git
- Docker (optional)
- Tesseract OCR (required for OCR features)

---

## Clone the Repository

```bash
git clone <repository-url>
cd Omni-Brain
```

---

## Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Run Tests

Execute all tests using:

```bash
pytest
```

---

## Run Pre-commit Checks

Run formatting and quality checks before pushing code:

```bash
pre-commit run --all-files
```

---

## Docker

Build and run the project:

```bash
docker compose up --build
```

---

## Git Workflow

Create a new feature branch:

```bash
git checkout -b feature/your-feature
```

Commit your changes:

```bash
git commit -m "type: short description"
```

Push the branch:

```bash
git push -u origin feature/your-feature
```

---

## Useful Commands

Update your branch:

```bash
git pull origin main
```

Check repository status:

```bash
git status
```

View commit history:

```bash
git log --oneline
```
