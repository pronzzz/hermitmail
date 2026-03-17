# Task 004: Local Knowledge Memory

## LLM Agent Directives

You are implementing Phase 4 to avoid re-summarizing previous articles and maintaining issue-to-issue memory.

**Goals:**

1. Set up a local vector database using FAISS.
2. Set up SQLite metadata store for hashes and deduplication.

**Rules:**

- DO NOT use cloud vector databases (Pinecone, etc.).
- Store text embeddings cleanly.

---

## Phase 1: Database Setup

### 1.1 Metadata Database

**File:** `src/knowledge/metadata_store.py`

Implement SQLite connection, schema initialization (URL, Hash, Date, Summary), and checking functions for deduplication.

### 1.2 Vector Database

**File:** `src/knowledge/vector_store.py`

Implement FAISS wrapper for storing embeddings and searching nearest neighbors. Include sentence-transformers for local embedding generation.

VERIFY: `venv/bin/python -m unittest tests/test_knowledge_db.py` passes.
