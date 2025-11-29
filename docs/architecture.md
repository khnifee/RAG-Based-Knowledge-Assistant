# Architecture Overview

This document provides a detailed explanation of the system architecture for the **RAG-Based Knowledge Assistant**. The project is designed to be modular, extensible, and aligned with production-level RAG system patterns. It includes an ingestion pipeline, vector search layer, conversation engine, and API services built using FastAPI and SQLAlchemy.

---

## 1. High-Level Architecture

The system consists of the following primary components:

- **Client Applications**
  - Web, CLI, or external backend services consuming the APIs.

- **API Layer (FastAPI)**
  - `/ingest` (future addition)
  - `/search`
  - `/chat`
  - Handles validation, dependency injection, and routing.

- **Ingestion Service**
  - Loads raw documents.
  - Extracts metadata.
  - Chunks text into semantic units.
  - Generates embeddings for each chunk.
  - Stores data in the relational database.

- **Vector Store / Embedding Store**
  - Stores chunk embeddings.
  - Performs vector similarity search.
  - Current implementation uses SQLite JSON fields.
  - Future versions can integrate FAISS / Qdrant / Weaviate.

- **Database Layer (SQLAlchemy ORM)**
  - Stores documents, chunks, embeddings, conversations, and messages.

- **RAG Engine**
  - Retrieves relevant chunks.
  - Optionally re-ranks results.
  - Generates final LLM response using context.

---

## 2. Component Diagram (Conceptual Description)

Below is a conceptual mapping of components (intended to pair with your draw.io diagram):

- Clients → FastAPI → Ingestion Service → Chunker / Embedding Service → DB
- Clients → FastAPI → Search Service → Vector Store → DB
- Clients → FastAPI → Chat Service → RAG Engine → LLM → DB

Connections:
- The ingestion path flows left-to-right from client → API → ingestion → DB.
- The search path flows client → API → vector store → DB.
- The chat path flows client → API → conversation manager → RAG engine → LLM → DB.

---

## 3. Module Architecture

The codebase is organized by functional layers inside the `app/` directory:

```
app/
  api/                  # API endpoints and request models
  core/                 # Configurations, constants, and base interfaces
  db/                   # SQLAlchemy models and session management
  services/             # Chunking, embedding, vector search, LLM integration
  utils/                # Helpers and reusable utilities
  ingest.py             # Document ingestion entrypoint
  main.py               # FastAPI bootstrap
```

Each service follows a clean abstraction:

- **Chunking Service**
  - Converts long documents into structured, retrievable segments.

- **Embedding Service**
  - Generates embeddings using OpenAI or HuggingFace models.

- **Vector Store Service**
  - Stores embeddings and performs similarity search.
  - Current backend: SQLite JSON.
  - Swappable backend: FAISS, Qdrant, Pinecone.

- **Generation Service**
  - Wraps the LLM for producing final responses.

- **Storage Service**
  - Handles persistence of documents, chunks, conversations, and messages.

---

## 4. Database Schema

The SQLAlchemy schema includes the following core tables:

### documents
- `id`
- `name`
- `path`
- `created_at`
- `document_metadata` (JSON)

### chunks
- `id`
- `document_id`
- `chunk_index`
- `text`
- `embedding` (JSON)
- `chunk_metadata` (JSON)

### conversations
- `id` (UUID)
- `knowledge_base_id`
- `created_at`

### messages
- `id`
- `conversation_id`
- `role`
- `content`
- `created_at`

Indexes:
- `(document_id, chunk_index)`
- `(conversation_id, created_at)`
- `created_at`
- `name`

---

## 5. RAG Workflow

### Step 1: Ingestion
- Document is loaded from filesystem.
- Text is extracted and normalized.
- Chunker splits text into semantically meaningful blocks.
- Embedding service generates vectors for each chunk.
- Database stores chunks and embeddings.

### Step 2: Search
- User query is embedded.
- Vector store computes similarity.
- Top chunks are returned with scores.

### Step 3: Chat
- Multi-turn conversation is preserved.
- Retrieval stage gathers relevant context.
- RAG Engine constructs prompt:
  - user message
  - retrieved supporting text
  - conversation history (optional)
- LLM generates response.
- Message is stored.

---

## 6. Future Improvements

- Migrate embeddings to a dedicated vector database.
- Add `/ingest` public API endpoint with async background tasks.
- Implement hybrid retrieval (dense + keyword-based).
- Add streaming LLM responses (Server-Sent Events).
- Support multiple knowledge bases per user.
- Conversation summarization to reduce token usage.
- Add retry, caching, and fault-tolerance middleware.

---

## 7. Design Principles

This project follows four guiding principles:

### Modularity
Each service is independent and replaceable.

### Extensibility
All major components use interface-based design for future plug-and-play backends.

### Observability
Structured logs and clear error boundaries improve debugging and traceability.

### Production Readiness
Includes:
- typing
- tests
- separation of concerns
- documented architecture
- API-first design

---

## 8. Maintainer

Towseef Altaf  
Software Engineer – Distributed Systems & AI Systems Architecture
