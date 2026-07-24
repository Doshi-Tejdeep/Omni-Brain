# OmniBrain Development Setup

This guide explains how to set up the OmniBrain project for local development.

## Prerequisites

- Python 3.12 or later
- Git
- Docker Desktop (optional)

## Clone the Repository

```bash
git clone https://github.com/Doshi-Tejdeep/Omni-Brain.git
cd Omni-Brain
```

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

## Run Tests

```bash
pytest
```

## Run Pre-commit Hooks

```bash
pre-commit run --all-files
```

## Project Structure

- `backend/` – Backend services
- `frontend/` – Streamlit frontend
- `docs/` – Project documentation
- `tests/` – Automated tests
