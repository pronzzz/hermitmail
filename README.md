# HermitMail 🧙‍♂️

<p align="center">
  <em>Curate like a wizard. Publish like a monk.</em><br/>
  An <strong>offline-first, privacy-respecting newsletter generator</strong> that ingests URLs, extracts content, summarizes via a local LLM, and produces a polished static newsletter. No SaaS lock-in. No tracking pixels. No email API circus.
</p>

---

## 🚀 Features

- **Offline-First & Local LLM**: Summarization is powered entirely by localized Ollama (LLaMA-3-8B). No OpenAI/Anthropic cloud dependencies.
- **Robust Scraping**: Uses `trafilatura` for highest-confidence text extraction, securely falling back to `readability-lxml` + BeautifulSoup to strip all potential malicious JavaScript/trackers.
- **Deduplication Engine**: A local SQLite Metadata Store ensures you never summarize the same URL twice across different newsletter editions.
- **Semantic Clustering**: Utizilizes FAISS and `sentence-transformers` for offline vector embeddings, which allows grouping articles into thematic clusters natively.
- **No-Tracking Static Outputs**: Generates purely static HTML and Markdown. Zero Javascript. Zero external network calls.
- **Weak-Machine Compatible**: Uses dynamic chunking to prevent out-of-memory errors.

## 📦 Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) (Must be running locally with `llama3:8b` pulled)

## 🛠️ Installation

```bash
git clone https://github.com/pronzzz/hermitmail.git
cd hermitmail
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **Note**: Ensure Ollama is running (`ollama serve`) and the model is downloaded (`ollama pull llama3:8b`).

## 🖥️ Usage

HermitMail uses a multi-phase CLI for deterministic execution:

1. **Ingest URLs (RSS Supported)**

   ```bash
   python src/main.py ingest --url https://example.com/article
   # Or from a file
   python src/main.py ingest --file list_of_links.txt
   ```

2. **Scrape Raw Text**

   ```bash
   python src/main.py scrape
   ```

3. **Summarize using Local LLM**

   ```bash
   python src/main.py summarize
   ```

4. **Cluster Themes and Build Static Output**

   ```bash
   python src/main.py build
   ```

Check your directory for the outputs (e.g., `issue_2026-03-18.html` and `.md`).

## 🧱 Project Structure

- `src/ingestion`: URL normalizing and RSS parsing.
- `src/scraping`: Content extraction & HTML sanitization.
- `src/summarization`: Ollama integration for LLaMA-3.
- `src/knowledge`: SQLite metadata and FAISS vector databases.
- `src/clustering`: K-Means clustering and LLM section header generation.
- `src/composer`: Jinja2 Static HTML/MD builder.
- `.tasks/`: Initial LLM execution specifications and architectural roadmap.

## 🤝 Contributing & Guidelines

Please refer to the enclosed [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) files for info on how to get involved. A more comprehensive [GUIDE.md](GUIDE.md) provides an overview on local development.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
