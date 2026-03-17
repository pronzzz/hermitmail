# HermitMail - Developer Guide

This guide describes the architecture and internal workings of HermitMail for anyone looking to extend the source code.

## Architecture

HermitMail is divided into six strictly modular phases that operate consecutively to avoid out-of-memory overhead and simplify testing.

1. **Ingestion Engine**: Reads URLs, strips Google Analytics tracking parameters (`utm_*`, etc.), removes hashes, and stores the canonical URL. Also scans basic XML RSS feeds for rapid batch loading.
2. **Scraping Engine**: Fetches HTML and uses `trafilatura` for main-content identification. Fallback to `readability-lxml`. Relies on `BeautifulSoup` to strip script tags completely. Treats all remote text as untrusted.
3. **Summarization Engine**: Interfaces with `ollama`. We specifically enforce strict "extraction-only" prompts to ensure the LLM never hallucinates data that was not present in the original scrape.
4. **Knowledge System**: 
   - Uses SQLite to track exactly which URLs have already been scraped and summarzed.
   - Uses `faiss-cpu` and `sentence-transformers` for embedding strings locally into persistent `.faiss` vector arrays.
5. **Clustering Engine**: Performs KMeans clustering over embeddings to automatically group random links (e.g. 5 tech articles, 2 finance articles) into sections. The LLM is invoked one final time to name these sections dynamically.
6. **Newsletter Composer**: Combines clustered objects with Jinja2 to output `.html` and `.md`.

## Managing State
Because HermitMail is completely serverless, the database is a local `hermitmail.sqlite3` file and `hermitmail.faiss` index. These are ignored by Git. 
If an operation fails midway (e.g. Ollama times out), it is safe to re-run the `summarize` CLI command; the SQLite DB will only target rows where `summary IS NULL`.

## Adding Extractor Support
If creating new scraping support in `src/scraping/extractor.py`, ensure that NO python `eval()` or `exec()` touches remote text, and that the returned dictionary always outputs plain unrendered text.
