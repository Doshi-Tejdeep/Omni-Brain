# OmniBrain - Agents Planning

## Objective
Plan the AI agents used in the OmniBrain Multi-Modal RAG system.

## Agent Architecture

### 1. Upload Agent
Responsibilities:
- Receive uploaded files
- Validate file type
- Store files

Input:
- PDF/Image

Output:
- Stored document

---

### 2. Document Processing Agent
Responsibilities:
- Parse PDF
- OCR images
- Extract tables
- Extract metadata
- Chunk text

Output:
- Processed chunks

---

### 3. Embedding Agent
Responsibilities:
- Generate embeddings
- Store vectors in database

Output:
- Vector database entries

---

### 4. Search Agent
Responsibilities:
- Search relevant chunks
- Return top matching documents

Output:
- Retrieved context

---

### 5. RAG Agent
Responsibilities:
- Combine retrieved context
- Build prompt
- Generate answer using LLM

Output:
- Final response

---

### 6. Vision Agent
Responsibilities:
- Analyze uploaded images
- Extract visual information

Output:
- Image description

---

### 7. SQL Agent
Responsibilities:
- Query structured database
- Return database results

Output:
- Structured response

---

## Workflow

Upload
↓
Document Processing
↓
Embedding
↓
Vector Database
↓
Search
↓
RAG
↓
Final Answer