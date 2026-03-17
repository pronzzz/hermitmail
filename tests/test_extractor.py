import unittest
from unittest.mock import patch
from src.scraping.extractor import fetch_and_extract

class TestExtractor(unittest.TestCase):
    @patch('src.scraping.extractor.trafilatura.fetch_url')
    @patch('src.scraping.extractor.trafilatura.extract')
    def test_trafilatura_extraction(self, mock_extract, mock_fetch):
        mock_fetch.return_value = "<html><body>Fake HTML</body></html>"
        mock_extract.return_value = '{"title": "Test Title", "author": "Alice", "date": "2026-01-01", "text": "This is the main text."}'
        
        result = fetch_and_extract("https://example.com/test")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Title")
        self.assertEqual(result["text"], "This is the main text.")
        self.assertEqual(result["author"], "Alice")

    @patch('src.scraping.extractor.trafilatura.fetch_url')
    @patch('src.scraping.extractor.trafilatura.extract')
    def test_readability_fallback(self, mock_extract, mock_fetch):
        # Readability fallback test
        html = """
        <html>
            <head><title>Fallback Title</title></head>
            <body>
                <div>Ignore this</div>
                <div id="readability-page-1">This is the actual important content.</div>
                <script>alert('bad');</script>
            </body>
        </html>
        """
        mock_fetch.return_value = html
        mock_extract.return_value = None # Force fallback
        
        result = fetch_and_extract("https://example.com/fallback")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Fallback Title")
        # Ensure scripts are stripped and content is extracted
        self.assertIn("This is the actual important content", result["text"])
        self.assertNotIn("alert('bad')", result["text"])

    @patch('src.scraping.extractor.trafilatura.fetch_url')
    def test_fetch_failure(self, mock_fetch):
        mock_fetch.return_value = None
        result = fetch_and_extract("https://example.com/fail")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
