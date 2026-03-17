import trafilatura
from readability import Document
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

def fetch_and_extract(url: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a URL and extracts the main content securely.
    Uses trafilatura primarily, falls back to readability-lxml.
    Returns plain text stripped of HTML tags to prevent injection.
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None

    # Try trafilatura first
    result = trafilatura.extract(
        downloaded,
        include_images=False,
        include_links=False,
        include_comments=False,
        output_format="json"
    )

    if result:
        import json
        data = json.loads(result)
        return {
            "title": data.get("title") or "Extracted Article",
            "author": data.get("author", ""),
            "date": data.get("date", ""),
            "text": data.get("text", ""),
            "url": url
        }

    # Fallback to readability-lxml
    doc = Document(downloaded)
    if doc.summary():
        # Clean HTML completely using BeautifulSoup
        soup = BeautifulSoup(doc.summary(), 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return {
            "title": doc.title() or "Extracted Article",
            "author": "", # Readability doesn't easily extract author
            "date": "",   # Readability doesn't easily extract date
            "text": text,
            "url": url
        }

    return None
