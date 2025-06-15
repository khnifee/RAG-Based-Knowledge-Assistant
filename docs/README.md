# RAG System – Database Schema

This document provides an overview of the database schema powering the Retrieval-Augmented Generation (RAG) system. The schema is built with SQLAlchemy and supports document ingestion, semantic chunking, vector embeddings, and conversational logging.

---

## Entity Relationship Diagram (ERD)

The following diagram visualizes the relationships between the core entities in the system.

> **Note:** Click the image to view full-size.

![ER Diagram](https://uml.planttext.com/plantuml/png/bPJVRzCm4CVV_LVS6o1MYUTgL9jKG0E9JUtU8oU-9LRzexAlR83utpaxQ-i6bYvvYNC_xEzzxkAhI3BGpXhHQONGwD0O576ZtLO6QQ4nCiPheg3h7U5DuzrQ_qBuK8GOxP1-RX5yeCuBqcGGFgrWgMMR_8-QEhXn2fymmeCFiBh-0kkcGok5U0CVNtxOgtopi-We0icQbOt7PxL5pcy1y1wqWZaB86mnmENbtRV58jkTjCYUDHVdscpPIfPwOca2Ia9LIMBxafVtscBsx4-fB99KaYG7V5tVVXT_X72U489kEmB_SDJ3USySvhoSiR3yIZhoudYOGASWxNAUKDFjt6OAdkU4SJQ7wWO1d_S1UPTAftAE0Tb3-9HWtVChVwEjKIa6kWSqphNV-2pKleeNY1RgUx17iKFGwVDj4NzH1h-RqWVlVc28ahHtazfnabTqfP_2iYaRvnyDgXQhMaQiYgWHfl-IAm_y3y3NbsmnHjdYb6eFAUFZLsgiJcaS9Z1uC_XzEOkuY-NmlPB9NjOGnq17Foq3uqLno9I1MQ7fUz3fRJm7h_zdPxD5SRlDeKRZNSlylJY0JJ6dCpNdUosaCeMuOddfilyB)

---

## Tables Overview

### `documents`
Stores metadata about ingested source files.

| Column            | Type     | Description                                  |
|-------------------|----------|----------------------------------------------|
| `id`              | Integer  | Primary key                                  |
| `name`            | String   | Name of the document                         |
| `path`            | String   | File system or storage path                  |
| `created_at`      | DateTime | Ingestion timestamp                          |
| `document_metadata` | JSON  | Metadata (tags, source, etc.)                 |

**Indexes:**
- `id` (PK)
- `name`
- `created_at`

---

### `chunks`
Semantic portions of a document with embeddings and metadata.

| Column          | Type     | Description                                  |
|------------------|----------|---------------------------------------------|
| `id`            | Integer  | Primary key                                  |
| `document_id`   | Integer  | Foreign key → `documents.id`                 |
| `chunk_index`   | Integer  | Index/order within document                  |
| `text`          | Text     | The actual chunk content                     |
| `embedding`     | JSON     | Vector representation                        |
| `created_at`    | DateTime | Creation timestamp                           |
| `chunk_metadata`| JSON     | Additional metadata (section, page, etc.)    |

**Indexes:**
- `document_id`
- `chunk_index`
- `created_at`
- Composite: `(document_id, chunk_index)`

---

### `conversations`
Tracks a user’s interaction session with the assistant.

| Column             | Type     | Description                              |
|--------------------|----------|------------------------------------------|
| `id`               | String   | UUID Primary key                         |
| `knowledge_base_id`| String   | Optional reference to a knowledge base   |
| `created_at`       | DateTime | Session start time                       |

**Indexes:**
- `id` (PK)

---

### `messages`
Stores messages exchanged during a conversation.

| Column           | Type     | Description                                |
|------------------|----------|--------------------------------------------|
| `id`            | Integer  | Primary key                                 |
| `conversation_id`| String   | Foreign key → `conversations.id`           |
| `role`          | String   | Sender role (`user`, `assistant`, `system`) |
| `content`       | Text     | Message text                                |
| `created_at`    | DateTime | Timestamp                                   |

**Indexes:**
- `conversation_id`
- Composite: `(conversation_id, created_at)`

---

## Design Notes

- **Timestamps use `datetime.utcnow` (UTC):**  
  Ensures all timestamps are timezone-neutral and consistent across systems and services, especially in distributed environments or when analyzing logs.

- **Embeddings and metadata fields stored as `JSON`:**  
  Using `JSON` allows flexibility in storing variable-length embeddings and extensible metadata (e.g., tags, section info, page numbers) without requiring rigid schema changes for every new field.

- **SQLAlchemy `relationship` with `cascade="all, delete-orphan"`:**  
  Ensures that related `chunks` and `messages` are automatically deleted when their parent (`document` or `conversation`) is deleted. This avoids orphaned data and maintains referential integrity.

- **Indexes are defined for query optimization:**  
  - `conversation_id` and `(conversation_id, created_at)` support fast retrieval of messages sorted by time within a session.
  - `document_id` and `(document_id, chunk_index)` allow efficient chunk retrieval in order from a document.
  - Indexing `name`, `created_at`, etc., enables quick filtering or recent document lookups.
  
  These indexes were chosen based on expected access patterns.

- **UUIDs used for Conversation IDs:**  
  Provides globally unique IDs that are non-predictable and safe to use across distributed systems, unlike auto-incrementing integers which can leak order or internal system size.

- **Normalized schema with one-to-many relationships:**  
  Documents and Conversations are modeled as parent entities with Chunks and Messages as children, which reflects the natural structure of the domain and simplifies retrieval logic.

- **Embedding stored directly in database (`JSON`) vs vector DB (for now):**  
  Chosen for simplicity and flexibility in early stages. In production, embeddings could be offloaded to a vector store (e.g., FAISS, Qdrant) for faster similarity search.

## Future Improvements

### 1. **Embeddings (Currently stored as JSON)**
**Current Approach:**  
Embeddings are stored in a `JSON` column for flexibility and easy prototyping, especially useful when not yet using a vector database.

**Limitations:**  
- SQL databases are not optimized for high-dimensional vector similarity search (e.g., cosine similarity).
- Cannot leverage ANN (Approximate Nearest Neighbor) algorithms for fast retrieval.
- Full-table scans are required unless integrated with an external service.

**Future Improvement:**  
- Migrate embedding storage and similarity search to a **vector database** like:
  - [FAISS](https://github.com/facebookresearch/faiss)
  - [Qdrant](https://qdrant.tech/)
  - [Pinecone](https://www.pinecone.io/)
  - [Weaviate](https://weaviate.io/)
- Store only the `chunk_id` and metadata in the relational DB; the actual vectors reside in the vector store.
- Add synchronization layer between the DB and vector index to keep results consistent.

---

### 2. **Metadata (Currently stored as JSON)**
**Current Approach:**  
Chunk- and document-level metadata is stored as semi-structured JSON to accommodate variable fields like section titles, page numbers, tags, and source origin.

**Limitations:**  
- Harder to query and index specific metadata fields (e.g., `tags`, `page_number`).
- No schema enforcement — increases risk of inconsistent data structures.

**Future Improvement:**  
- **Schema-normalize** high-value metadata fields into separate columns or related tables (e.g., `tags`, `source_type`, `page_number`).
- Use **JSON Schema validation** on write, if sticking with JSON format, to enforce structure.
- If metadata becomes query-critical, consider creating a dedicated `Metadata` table with relationships.

---

### General Notes
- The current approach trades off **query performance** and **consistency** for **developer agility** and **flexibility**.
- Future improvements can be incremental — start with migrating only high-frequency queried metadata or embeddings.



---

## Tools Used

- **SQLAlchemy** – Python ORM
- **PlantUML** – ER diagram generation
- **PostgreSQL** (recommended) – Backend relational DB engine

---

# RAG Service Architecture

This project is a modular and extensible implementation of a Retrieval-Augmented Generation (RAG) system. The components are separated by functionality and layered cleanly to support maintainability, testing, and pluggable design.

---

## Search Route Architecture

![Search Component Diagram](https://www.plantuml.com/plantuml/png/VLHFQ_f04BtlfnWywK5-znyI_6DB1QN5G2yboBePOZ3PJNStGcZxtHkp6jCre-31D-yzPzuaCpMMQrlc6JF7L1PSyno4oWibKThGLXc2Hc6vJ39apAQs1aBaMXnWgqgBiBYIOOacJIGC_vccFcAiuEB84uJ1x6q5QrwXXk4pDxR-EHh05uFwy-7Oe1ktLXonduu-H7rA1JgFLlcKxp6EKvbSof63tr5OfSFwYssXQzRAFBivD-Xgg2EOJFZUMCs53G9NNol1ivRWiDS2vMpbWGdQ7LwWOJq9qIsCny4T6Vv3ZHYuGhsEJkdtGnBxclJKCFuEN0BqW1IlcwtB7fhmU-BjhAOluPNSOAvqrQMvoakrrsbyZo_dFkOoE3NepfpXsmewN7y9leJsSWgwLK92pa0BlE7eZ6vReP8ZsNIUDBExy8sACJFjajrfsE9dYSP6Vp5JA6dQFrAYp57QnQ6KnyQIE0Gk2z_uCTb_rHxp-oy6_R1uhJ-szeVtW7vBDaKPds_oBm00)

---

## Chat Route Architecture

![Chat Component Diagram](https://www.plantuml.com/plantuml/png/XLJBRjim4BphAuYSuaFG7mYC-96c1kmcbO5UYi2WfOL2c29LaWfWjFdtqlA6eBShs80FcftLpinIVF11kj2tkl07PJhfP2igstRMW0dRSDGW75H1caP34LI8pr-gDnb4QVi0Ol595KlmgZ7YzckljIXdJ-95TQ2LWKbHTB8wo0R4pUnb9TRo22xof0_nSN8Z_XGY_duDRtN3Ms-74PFNuYFhtTWQj4_qHMIKyBi77rvpn4Sz7Z9e0zxBvXDPsgflmOJ5MsyEbmDEPB45zwugEAjCmqhPO05VimtMnQPBy0aCE1ahbt0PGHF3RH8yQbZStKqvQwDKAcoSoQUJ86IHm5WIpP16XAp7TWzrdTlcUJ-XEaKM_t25IKFdMVmMA8zRItuOadfo4aPSDH1sC9J0tKuGNDjAwaT44NlkmCnM19nB3maIz_ToxuEJLPXE2sugMk2d4X2PZ1IEoEeZtP7uTqeqCzvuNXxnUV5Ys3n9cJyJgFbzAExygPfShym6MkkEMITMlXttJjN_uyivmN0H6Shk8gkJRV3Qk09sSAAljF1knXiOc-pSR5lN8kJPVB0yatnh-5tdPm0T-NDbjuzKC7LATFjZhG9WNxOxHDYzOOtkR7G8NyC-HW31acz4YETq-p2ktL3BFkbv0oLYY7otprqEeVy4SG6aaIG2PY81aKbby3IgZHZ8Wk4zZRFo_F2MLzOm0JRdeYLNCVROo_kAeCFCXB51fYe9afrCKEGoUdWggv8QokFYJLvXVXGFOEg-rVy0)

---

## Ingestion Pipeline Architecture

![Ingestion Component Diagram](https://www.plantuml.com/plantuml/png/VLFHQXin47pNLonvQGk9eUrR2IPfca8Wa1JJfnA2h1kVHNJIiTfBOzh-UwsSpZwiYnzlTdPtPavx4KMpT8rJySdwLhDko8Ic3HvU5h9n88OHxMi79LOSwCRNY6A3f-yk_AQhWKsNRDPMOAHZADLgywHhqCcUVszREEjnGdyK4T6lNUag1AwirnBuGVqRDL-jExyLLjEjte1tZGEy03zRWuSU_HPCry3BQnMSqQywOa3e_5mlex0sCf-hwLbqTZQVdbMYTFPtFjvmeFwwMQAgIlazNkYl8OzuBO7VVyZWRJ3QzGqx6NSj_END0PXKPAWqMcxDJYUt5c3FBALC4qjzfP5zSaUz5Rp3Y1SIMDSu23YZPRonBpmkj_tmrSxluiUj5UIsKQ0PAVCiboJhHvTCrt9VAU0GsoMnGr8GxsZgY2YmMIFf5KIIDQZDjwUcZow9A4_X2BbuJiVPnHzHFWY8RRqM2YkQRbLtOnjseAI6AbzYfENcY_eueq4xcU05NjIdBSRGaZ0CMgFwFADxSBGn5L8q3KcW_5iKV4L9MQ6lY6RHEYkH12z2rakWy0nskctJsC0KqMWlrcZdDgg1zbjyrJaoQL2aBYQUfjPrTQsN3dq1F7jRGvdupuX8Asqay2RPi3vAsge5z7fl55Zr5qN3bT9IHrGKV4fgPUkt5nO_BNqZxhC_pMvEHm7FrFMBm4URFAq2K_-AKoIhJZe6vQSVHuiluAkkSVy1)

---

## Notes

- All diagrams are generated using [PlantUML](https://plantuml.com/).
- You can regenerate or update diagrams via your CI or manually by updating the PlantUML source.

## API Structure

### `/search` (POST)

**Description**: Performs a semantic vector search over the knowledge base using the provided query.

#### Sample Request
```json
{
  "query": "When parties entered into that certain Master Services Agreement"
}
```

#### Sample Response
```json
{
  "query": "When parties entered into that certain Master Services Agreement",
  "results": [
    {
      "chunk_id": 15,
      "text": "MASTER SERVICES AGREEMENT This Master Services Agreement (this “Agreement”) is entered into on February 1, 2024...",
      "metadata": {
        "chunk_index": 0,
        "start_word": 0,
        "end_word": 149,
        "word_count": 150,
        "char_count": 1037,
        "format": "PDF 1.7",
        "creator": "Microsoft® Word 2021",
        "producer": "Microsoft® Word 2021",
        "creationDate": "D:20250527155618-07'00'",
        "modDate": "D:20250527155618-07'00'"
      },
      "similarity_score": 0.6266892250669005
    },
    ...
  ],
  "total_found": 5
}
```

---

### `/chat` (POST)

**Description**: Generates a conversational response using LLM. If knowledge base is enabled, it uses retrieved context from vector store.

#### Sample Request
```json
{
  "query": "where is the temprature of delhi",
  "conversation_id": "824db00a-ed3d-401d-839a-2a889efd9fc2"
}
```

#### Sample Response
```json
{
  "message": {
    "role": "assistant",
    "content": "I don’t know based on the provided context."
  },
  "conversation_id": "824db00a-ed3d-401d-839a-2a889efd9fc2",
  "created_at": "2025-06-15T13:10:33.972197",
  "sources": [
    {
      "chunk_id": 29,
      "text": "other terms and conditions of the MSA shall remain in full force and effect...",
      "metadata": {
        "chunk_index": 2,
        "start_word": 240,
        "end_word": 301,
        "word_count": 62,
        "char_count": 521,
        "format": "PDF 1.7",
        "creator": "Microsoft® Word 2021",
        "producer": "Microsoft® Word 2021",
        "creationDate": "D:20250527155618-07'00'",
        "modDate": "D:20250527155618-07'00'"
      },
      "similarity_score": 0.0698689272221555
    }
  ],
  "usage": null
}
```

---

> Tip: All APIs follow standard JSON request/response formats and return relevant metadata along with document chunks and similarity scores. These examples are simplified — responses can be customized based on your config and vector store implementation.

## Prerequisites

- Python 3.8+
- OpenAI API key (for embedding/generation services)
- Git (optional, for cloning the repo)

---

## Installation

### 1. Set up environment variables

Create a `.env` file inside the `app` directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

---

### 2. Create and activate a Python virtual environment

**On Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install required Python packages

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the ingestion pipeline

Process documents from the `sample_data` folder and populate the database:

```bash
python3 -m app.ingest
```

### Start the FastAPI service

Launch the API server locally with auto-reload for development:

```bash
uvicorn app.main:app --reload
```

---

## Accessing the API

Open your browser and navigate to:

```
http://localhost:8000
```

You can access the automatically generated API docs at:

```
http://localhost:8000/docs
```

---

## Project Structure

- `app/` — Application source code  
  - `ingest.py` — Ingestion pipeline runner  
  - `main.py` — FastAPI app entrypoint  
  - `logging_config.py` — Centralized logging setup  
  - `services/` — Embedding, chunking, storage, and generation services  
  - `api/` — API routes and dependency injection  
  - `db/` — SQLAlchemy models and database session management  
  - `utils/` — Utility functions and helpers used across the app  
  - `core/` — Core configs, constants, and shared abstractions  
- `sample_data/` — Example documents for ingestion  
- `tests/` — Unit and integration tests for services and APIs  
- `requirements.txt` — Python dependencies  
- `.env` — Environment variables (not committed to version control)

---


## Running Tests

To run tests locally, follow these steps:

1. **Create and activate a virtual environment**  
   - On **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the test suite using `pytest`**:
   ```bash
   python -m pytest
   ```

   For verbose output:
   ```bash
   python -m pytest -v
   ```

   To run a specific test file:
   ```bash
   python -m pytest tests/path/to/test_file.py
   ```

4. **(Optional)**: Run tests with coverage report:
   ```bash
   python -m pytest --cov=app tests/
   ```

---

