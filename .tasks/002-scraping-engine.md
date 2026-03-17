# Task 002: Scraping Engine

## LLM Agent Directives

You are implementing Phase 2 to extract content effectively using `trafilatura` and fallback to `readability-lxml`.

**Goals:**

1. Extract title, author, date, main content, canonical URL.
2. Strip ads, navigation, comments, scripts safely.

**Rules:**

- DO NOT execute any JavaScript.
- Treat all scraped text as untrusted.
- Strip HTML tags before text is returned for LLM processing.

---

## Phase 1: Trafilatura Integration

### 1.1 Setup Extractor

**File:** `src/scraping/extractor.py`

Implement a scraping function taking a normalized URL, fetching HTML, and using trafilatura to extract plain text and metadata.

VERIFY: Run extractor against a known sample article (saved locally) and assert expected text.
