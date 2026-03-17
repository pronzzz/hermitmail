# Task 001: Core Ingestion System

## LLM Agent Directives

You are implementing Phase 1 to achieve a local URL ingestion system for HermitMail.

**Goals:**

1. Accept URLs from manual input, text file, and basic RSS feeds.
2. Normalize URLs, remove tracking parameters, and canonicalize links.
3. Detect duplicates before proceeding.

**Rules:**

- DO NOT add new features outside ingestion.
- DO NOT use any cloud APIs.
- VERIFY by writing unit tests for URL normalization and RSS parsing.

---

## Phase 1: Setup Core Ingestion Module

### 1.1 Create URL Normalizer

**File:** `src/ingestion/normalizer.py`

Create a function to strip tracking parameters (e.g., `utm_source`, `ref`) and normalize URLs to their canonical form.

VERIFY: `venv/bin/python -m unittest tests/test_normalizer.py` passes.

---

## Phase 2: RSS Parsing

### 2.1 Basic RSS Ingestion

**File:** `src/ingestion/rss_parser.py`

Parse standard RSS/Atom feeds to extract article links without downloading the full content yet.

VERIFY: Pass a sample local RSS XML and verify extracted links.

---

## Checklist

### Phase 1

- [x] Create URL normalizer
- [x] Write unit tests for normalizer

### Phase 2

- [x] Implement local RSS XML parser
- [x] Write unit tests for RSS parser
