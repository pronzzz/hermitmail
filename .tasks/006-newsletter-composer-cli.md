# Task 006: Newsletter Composer and CLI

## LLM Agent Directives

You are implementing Phase 6 and 7 to generate the final HTML/Markdown newsletters and creating the CLI interface.

**Goals:**

1. Generate clean HTML and Markdown archives using Jinja2 templates.
2. Build the main CLI `hermitmail` to connect ingestion to static output.
3. Ensure reproducible and deterministic builds.

**Rules:**

- Outputs must be fully static (Zero JS, No tracking code).
- Keep CSS minimal and print-friendly.

---

## Phase 1: Templating Engine

### 1.1 HTML/Markdown Generation

**File:** `src/composer/templates.py` and `src/templates/issue.html`

Setup Jinja2 to render the final issue from the structured clusters and summaries.

---

## Phase 2: CLI Interface

### 2.1 Argparse CLI

**File:** `src/main.py`

Implement argparse for commands: `ingest`, `scrape`, `summarize`, `cluster`, `build`.

VERIFY: `venv/bin/python src/main.py --help` shows correctly.
