# OmniBrain: Agentic Multi-Modal RAG Orchestrator

## Overview

OmniBrain is an AI-powered Agentic Multi-Modal Retrieval-Augmented Generation (RAG) system that enables users to upload documents and interact with them using natural language.

Instead of manually searching through documents, users can ask questions in plain English. OmniBrain processes documents, retrieves relevant information using semantic search, and generates context-aware answers using Large Language Models.

The project combines:

- Document Processing
- Embeddings
- Vector Search
- Retrieval-Augmented Generation (RAG)
- Agentic AI workflows
- LLM-based Question Answering

---

# Key Features

## Document Processing

- PDF document upload
- Text extraction using PyMuPDF
- Intelligent text chunking
- Metadata extraction
- OCR support
- Page-level source tracking

## AI & RAG Pipeline

- Semantic embedding generation
- ChromaDB vector storage
- Similarity-based retrieval
- Context-aware answer generation
- Ollama LLM integration
- Source citation support

## Application Features

- FastAPI backend
- Streamlit frontend
- REST API support
- Docker deployment support
- Automated testing with Pytest

---

# System Architecture

```
                User
                  |
                  |
            Upload PDF
                  |
                  ↓
          FastAPI Upload API
                  |
                  ↓
       Document Processing Pipeline
                  |
        -------------------------
        |           |           |
   Extraction   Chunking   Metadata
        |
        ↓
  Embedding Generation
        |
        ↓
      ChromaDB
   Vector Database
        |
        ↓
      Retriever
        |
        ↓
     Ollama LLM
        |
        ↓
   Answer + Sources
```

---

# Tech Stack

## Frontend

- Streamlit

## Backend

- Python
- FastAPI

## AI / RAG

- LangChain
- Ollama
- Embedding Models

## Vector Database

- ChromaDB

## Document Processing

- PyMuPDF
- Tesseract OCR

## DevOps

- Docker
- Docker Compose
- GitHub Actions
- Pytest

---

# Project Structure

```
Omni-Brain/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── document_processing/
│   │   ├── pdf_parser.py
│   │   ├── chunker.py
│   │   ├── metadata_extractor.py
│   │   ├── image_extractor.py
│   │   └── ocr_extractor.py
│   │
│   └── vector_db/
│       ├── embeddings.py
│       └── vector_store.py
│
├── frontend/
│
├── tests/
│
├── docs/
│
├── sample_data/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd Omni-Brain
```

## Create Virtual Environment

```bash
python -m venv .venv

source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Start Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

Backend URL:

```
http://127.0.0.1:8000
```

API Documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Upload Document

### Endpoint

```
POST /upload
```

Workflow:

```
PDF Upload
     |
     ↓
Text Extraction
     |
     ↓
Chunk Creation
     |
     ↓
Embedding Generation
     |
     ↓
ChromaDB Storage
```

---

## Ask Questions

### Endpoint

```
POST /ask
```

Example Request:

```json
{
  "question": "What is OmniBrain?"
}
```

Example Response:

```json
{
  "question": "What is OmniBrain?",
  "answer": {
    "answer": "OmniBrain is an Agentic Multi Modal RAG Orchestrator.",
    "sources": [
      "Page 1"
    ]
  }
}
```

---

# Testing

Run all tests:

```bash
python -m pytest -v
```

Current test status:

```
14 tests passed
```

The test suite validates:

- PDF parsing
- Text chunking
- Metadata extraction
- OCR extraction
- Image extraction
- Table extraction
- End-to-end RAG pipeline

---

# Docker Setup

## Build Image

```bash
docker build -t omnibrain .
```

## Run Using Docker Compose

```bash
docker compose up --build
```

---

# Team Members

| Member | Role |
|---|---|
| D. Tejdeep | Team Lead |
| Saumaditya | Backend |
| Pavan | Frontend |
| Rishi | Document Processing |
| Mariam | AI/RAG |
| Teja | Database |
| Sunishka | DevOps/QA |

---

# Development Workflow

```
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
Monitoring
```

---

# Completed Milestones

✅ Document Processing Pipeline
✅ PDF Text Extraction
✅ Intelligent Chunking
✅ Metadata Handling
✅ OCR Support
✅ Embedding Generation
✅ ChromaDB Vector Storage
✅ RAG Retrieval Pipeline
✅ Ollama LLM Integration
✅ Source Citations
✅ End-to-End Integration Testing

---

# Release Status

## OmniBrain v1.0

Status:

```
Production Ready MVP
```
