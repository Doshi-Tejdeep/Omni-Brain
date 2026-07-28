 #Title Of the Project
"OmniBrain": Agentic Multi-Modal RAG Orchestrator
# Omni-Brain Description
OmniBrain is an AI-powered assistant that integrates multiple AI models to provide intelligent conversations, task automation, code generation, document analysis, and productivity tools through a user-friendly interface.
Omni Brain is an AI-powered knowledge management and question-answering platform that enables users to upload documents and interact with them using natural language. Instead of manually searching through files, users can ask questions in plain English, and the system retrieves the most relevant information from the uploaded documents using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

The project combines document processing, semantic search, vector databases, and generative AI to create an intelligent assistant capable of understanding document content and providing context-aware responses.
# Features of Omni-Brain

- Upload PDF documents
- Intelligent document parsing
- AI-powered question answering
- Chat interface
- FastAPI backend
- Streamlit frontend
- Database storage
- Docker support
- # Tech stacks used to create a Omni Brain
- Frontend
- Streamlit

Backend
- FastAPI

AI
- LangChain
- OpenAI/Ollama

Database
- SQLite / PostgreSQL

DevOps
- Docker
- Docker Compose
- GitHub Actions
- Pre-commit

#Folder Structure of the Omni Brain Project
- Omni-Brain/
-
-├── backend/

-├── frontend/

-├── docs/

-├── tests/

-├── sample_data/

-├── Dockerfile

-├── docker-compose.yml

-├── README.md

-└── requirements.txt

# Progress of Installation
git clone <repository-url>

cd Omni-Brain

python -m venv venv

pip install -r requirements.txt
# To run the Backend of the project Omni Brain project
cd backend

uvicorn app.main:app --reload
# To run the Frontend of the project Omni Brain project
streamlit run frontend/app.py
# To run the Docker of the project Omni Brain project
docker compose up --build
# Omni Brain Project creators Team Members
| Member     | Role                |
| ---------- | ------------------- |
| D. Tejdeep | Team Lead           |
| Saumaditya | Backend             |
| Pavan      | Frontend            |
| Rishi      | Document Processing |
| Mariam     | AI/RAG              |
| Teja       | Database            |
| Sunishka   | DevOps/QA           |
# Development Workflow
Requirement Analysis

        ↓

System Design

        ↓

Development

        ↓

Integration

        ↓

Testing

        ↓

Deployment

        ↓

Monitoring & Maintenance
# Testing
pytest

# Docker

## Prerequisites

- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- Docker Compose

## Build the Docker Image

```bash
docker build -t omnibrain .
```

## Run the Test Container

```bash
docker run --rm omnibrain
```

## Run with Docker Compose

```bash
docker compose up
```

## Notes

- Run all commands from the project root directory.
- The current Docker configuration is intended for testing and development.
- Docker Compose uses the `qa` service defined in `docker-compose.yml`.

## Additional Documentation

- `docs/development-setup.md` – Local development environment setup.
