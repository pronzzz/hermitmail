# Task 005: Clustering & Theme Detection

## LLM Agent Directives

You are implementing Phase 5 to group articles into topical sections.

**Goals:**

1. Group articles using K-means or Hierarchical clustering on their embeddings.
2. Generate suggested section headings using the local LLM.

**Rules:**

- Use purely local processing (scikit-learn or similar is acceptable, or FAISS-based clustering).

---

## Phase 1: Clustering implementation

### 1.1 Grouping Logic

**File:** `src/clustering/grouper.py`

Implement topic clustering using article embeddings and use `LocalLLMClient` to summarize the cluster into a short section heading.

VERIFY: `venv/bin/python -m unittest tests/test_clustering.py` passes.
