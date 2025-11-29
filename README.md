# Retrieval-Augmented Generation (RAG) Pipeline

This repository implements a modular Retrieval-Augmented Generation (RAG) system with a complete ingestion workflow, semantic text chunking, embedding generation, vector search, and multi-turn conversational capabilities. The system is designed with extensibility and maintainability in mind, using FastAPI, SQLAlchemy, and OpenAI models.

---

## Architecture Overview

The system is composed of independent but connected subsystems:

- **Ingestion Pipeline** — loads documents, extracts metadata, chunks text, and generates embeddings.
- **Vector Search Engine** — performs similarity search using stored embeddings.
- **Chat Pipeline** — orchestrates multi-turn conversations and optional retrieval.
- **Knowledge Store** — relational models for documents, chunks, embeddings, conversations, and messages.
- **API Gateway** — exposes `/ingest`, `/search`, and `/chat` endpoints.

A high-level architecture diagram is available below:

![High-Level Architecture](docs/HighLevelArchitecturalDiagram.png)

> Additional diagrams and design notes are available in the `docs/` directory.

---

## Features

- Document ingestion with metadata and structured storage  
- Semantic chunking optimized for embedding models  
- Embedding generation using OpenAI embedding APIs  
- Vector similarity search over chunked documents  
- Retrieval-augmented multi-turn chat completion  
- SQLAlchemy ORM modeling with UUID-based conversation sessions  
- Modular services layer for easy extension or substitution  
- RESTful API exposure via FastAPI  
- Extensible codebase structured for testing and integration

---

## Database Schema

The schema models the core elements of a RAG system.

### **documents**
Stores metadata for each ingested source file.

- `id`
- `name`
- `path`
- `created_at`
- `document_metadata` (JSON)

### **chunks**
Semantic text chunks with associated embeddings.

- `id`
- `document_id`
- `chunk_index`
- `text`
- `embedding` (JSON)
- `created_at`
- `chunk_metadata` (JSON)

### **conversations**
Represents a conversational session.

- `id` (UUID)
- `knowledge_base_id`
- `created_at`

### **messages**
Linked to conversations; stores user and assistant messages.

- `id`
- `conversation_id`
- `role`
- `content`
- `created_at`

Indexing is applied based on common retrieval patterns.

---

## API Endpoints

### **POST /ingest**
Processes documents and populates the knowledge base.

### **POST /search**
Performs semantic search over stored document embeddings.

**Request**
```json
{
  "query": "What does clause 7 describe?"
}
```

**Response**
```json
{
  "results": [...],
  "total_found": 5
}
```

---

### **POST /chat**
Generates a conversational response, optionally using retrieved context.

**Request**
```json
{
  "query": "Explain the confidentiality section",
  "conversation_id": "uuid"
}
```

---

## Project Structure

```
app/
  api/                # FastAPI route handlers
  core/               # Configurations and shared constants
  db/                 # SQLAlchemy models and database session
  ingest.py           # Ingestion workflow entry point
  logging_config.py   # Application-wide logging setup
  main.py             # FastAPI application bootstrap
  services/           # Embedding, chunking, retrieval, generation services
  utils/              # Common utilities
docs/
  architecture-diagram.png
  additional-design-docs.md
sample_data/
tests/
requirements.txt
```

---

## Running Locally

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set environment variables
Create `app/.env`:

```
OPENAI_API_KEY=your_api_key_here
```

### Run ingestion
```bash
python3 -m app.ingest
```

### Start the API server
```bash
uvicorn app.main:app --reload
```

Open API Documentation:

```
http://localhost:8000/docs
```

---

## Testing

### Run test suite
```bash
pytest
```

### With coverage
```bash
pytest --cov=app tests/
```

---

## Roadmap

- Integrate a dedicated vector database (FAISS, Qdrant, Weaviate)
- Add hybrid retrieval (dense + sparse)
- Stream responses for chat completions
- Implement ingestion via REST endpoint
- Add web-based admin dashboard
- Enhance conversation summarization

---

## License
MIT License

---

## Author
**Towseef Altaf**  
Software Engineer – Distributed Systems, Developer Productivity, AI Engineering
