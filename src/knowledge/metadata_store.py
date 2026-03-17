import sqlite3
import hashlib
from typing import Optional, Dict, Any

class MetadataStore:
    def __init__(self, db_path: str = "hermitmail.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    url_hash TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT,
                    summary TEXT,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            
    def _hash_url(self, url: str) -> str:
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def add_article(self, url: str, title: str, summary: str) -> bool:
        """
        Adds an article to the store. Returns True if added, False if it was already there.
        """
        url_hash = self._hash_url(url)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO articles (url_hash, url, title, summary) VALUES (?, ?, ?, ?)",
                    (url_hash, url, title, summary)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # UNIQUE constraint failed: article exists
            return False

    def get_article(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetches an article by URL if it exists, otherwise None.
        """
        url_hash = self._hash_url(url)
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE url_hash = ?", (url_hash,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
