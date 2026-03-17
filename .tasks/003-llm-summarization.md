# Task 003: Local LLM Summarization

## LLM Agent Directives

You are implementing Phase 3 to generate summaries using a local LLM via Ollama.

**Goals:**

1. Connect to local Ollama (Llama-3-8B).
2. Generate a 2-sentence summary per article with a neutral tone and strict extraction-based prompts.

**Rules:**

- DO NOT use OpenAI, Anthropic, or any cloud LLMs.
- Strictly prevent hallucinations by citing the article title and limiting creative output.

---

## Phase 1: Ollama Client Setup

### 1.1 Connect and Summarize

**File:** `src/summarization/llm_client.py`

Implement a class `LocalLLMClient` that takes cleaned text, constructs an extraction prompt, and calls the local Ollama API to get a 2-sentence summary.

VERIFY: `venv/bin/python -m unittest tests/test_llm_client.py` passes using a mocked or local test-only Ollama endpoint.
