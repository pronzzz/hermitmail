import argparse
import sys
import os
import datetime
from typing import List

# Ensure we can import from src when running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.normalizer import normalize_url
from src.ingestion.rss_parser import parse_rss_links
from src.scraping.extractor import fetch_and_extract
from src.summarization.llm_client import LocalLLMClient
from src.knowledge.metadata_store import MetadataStore
from src.knowledge.vector_store import VectorStore
from src.clustering.grouper import ClusteringEngine
from src.composer.templates import NewsletterComposer

def ingest_cmd(args):
    """
    Ingests URLs directly or from a file. If RSS is passed, extracts links first.
    Normalizes URLs and adds them to DB without scraping yet.
    """
    db = MetadataStore()
    urls_to_process = []
    
    if args.url:
        urls_to_process.append(args.url)
    if args.file:
        with open(args.file, 'r') as f:
            for line in f:
                if line.strip():
                    urls_to_process.append(line.strip())
                    
    for u in urls_to_process:
        norm_u = normalize_url(u)
        
        # Super basic RSS detection for CLI proof-of-concept
        if norm_u.endswith('.xml') or norm_u.endswith('rss'):
            # Fetch RSS (using trafilatura simply as a downloader here)
            import trafilatura
            xml_data = trafilatura.fetch_url(norm_u)
            if xml_data:
                rss_links = parse_rss_links(xml_data)
                for link in rss_links:
                    nl = normalize_url(link)
                    if db.add_article(nl, "", ""):
                        print(f"[INGEST] Added from RSS: {nl}")
                    else:
                        print(f"[INGEST] Skipped existing: {nl}")
        else:
            if db.add_article(norm_u, "", ""):
                print(f"[INGEST] Added: {norm_u}")
            else:
                print(f"[INGEST] Skipped existing: {norm_u}")

def scrape_cmd(args):
    """
    Finds ingested articles that have no title/summary yet, and scrapes them.
    Note: A robust queue system would be better here, this is basic iterating.
    """
    db = MetadataStore()
    vstore = VectorStore()
    
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM articles WHERE title = '' OR title IS NULL")
        rows = cursor.fetchall()
        
    if not rows:
        print("[SCRAPE] Nothing new to scrape.")
        return
        
    for row in rows:
        url = row[0]
        print(f"[SCRAPE] Extracting: {url}")
        data = fetch_and_extract(url)
        if data and data.get('text') and data.get('title'):
            print(f"[SCRAPE] Success. Title: {data['title']}")
            # Update DB with title temporarily
            with sqlite3.connect(db.db_path) as conn:
                cur = conn.cursor()
                cur.execute("UPDATE articles SET title = ? WHERE url = ?", (data['title'], url))
                conn.commit()
        else:
            print(f"[SCRAPE] Failed to extract from {url}. Data received: {bool(data)}")

def summarize_cmd(args):
    """
    Finds scraped articles with no summary, uses LLM to summarize, and stores.
    Also adds the summary embedding to the VectorStore.
    """
    db = MetadataStore()
    vstore = VectorStore()
    llm = LocalLLMClient()
    
    import sqlite3
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        # Find articles that have a title (scraped) but no summary
        cursor.execute("SELECT url, title FROM articles WHERE (summary = '' OR summary IS NULL) AND (title != '' AND title IS NOT NULL)")
        rows = cursor.fetchall()
        
    if not rows:
        print("[SUMMARIZE] Nothing new to summarize.")
        return
        
    for row in rows:
        url, title = row
        print(f"[SUMMARIZE] Summarizing via LLM: {title}")
        
        # We need the text. For a CLI run without huge intermediate DB, we re-fetch locally from cache if we stored it,
        # or we just re-extract here natively.
        # *Optimization*: In production, store raw_text in SQLite or disk to avoid re-fetching.
        data = fetch_and_extract(url) 
        if data and data['text']:
            summary = llm.summarize_article(title, data['text'])
            print(f" -> {summary}")
            
            # Save summary to DB
            with sqlite3.connect(db.db_path) as conn:
                cur = conn.cursor()
                cur.execute("UPDATE articles SET summary = ? WHERE url = ?", (summary, url))
                conn.commit()
                
            # Add to FAISS memory
            vstore.add_embeddings(url, summary)

def build_cmd(args):
    """
    Fetches all completed articles, clusters them, and outputs HTML & Markdown.
    """
    db = MetadataStore()
    
    import sqlite3
    articles = []
    with sqlite3.connect(db.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Get articles that have summaries
        cursor.execute("SELECT * FROM articles WHERE summary != '' AND summary IS NOT NULL")
        for row in cursor.fetchall():
            articles.append(dict(row))
            
    if not articles:
        print("[BUILD] No summarized articles to build.")
        return
        
    print(f"[BUILD] Clustering {len(articles)} articles...")
    engine = ClusteringEngine()
    groups = engine.group_articles(articles)
    
    composer = NewsletterComposer()
    issue_date = datetime.date.today().isoformat()
    
    html = composer.generate_html(issue_date, groups, "Welcome to this auto-generated edition of HermitMail.")
    md = composer.generate_markdown(issue_date, groups, "Welcome to this auto-generated edition of HermitMail.")
    
    html_file = f"issue_{issue_date}.html"
    md_file = f"issue_{issue_date}.md"
    
    with open(html_file, 'w') as f:
        f.write(html)
    with open(md_file, 'w') as f:
        f.write(md)
        
    print(f"[BUILD] Created {html_file}")
    print(f"[BUILD] Created {md_file}")

def main():
    parser = argparse.ArgumentParser(description="HermitMail: Offline-First Newsletter Generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Ingest
    parser_ingest = subparsers.add_parser('ingest', help='Ingest URLs into the local DB')
    parser_ingest.add_argument('--url', type=str, help='Single URL to ingest')
    parser_ingest.add_argument('--file', type=str, help='Text file with list of URLs')
    
    # Scrape
    parser_scrape = subparsers.add_parser('scrape', help='Extract content from pending URLs')
    
    # Summarize
    parser_summarize = subparsers.add_parser('summarize', help='Summarize scraped articles using local LLM')
    
    # Build
    parser_build = subparsers.add_parser('build', help='Cluster and build the static newsletter')
    
    args = parser.parse_args()
    
    if args.command == 'ingest':
        ingest_cmd(args)
    elif args.command == 'scrape':
        scrape_cmd(args)
    elif args.command == 'summarize':
        summarize_cmd(args)
    elif args.command == 'build':
        build_cmd(args)

if __name__ == '__main__':
    main()
