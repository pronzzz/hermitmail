import unittest
from src.ingestion.normalizer import normalize_url

class TestNormalizer(unittest.TestCase):
    def test_strip_tracking_params(self):
        url = "https://example.com/article?utm_source=twitter&utm_medium=social&v=123"
        expected = "https://example.com/article?v=123"
        self.assertEqual(normalize_url(url), expected)

    def test_strip_fragment(self):
        url = "https://example.com/page#section1"
        expected = "https://example.com/page"
        self.assertEqual(normalize_url(url), expected)

    def test_ensure_scheme(self):
        url = "example.com/post"
        expected = "https://example.com/post"
        self.assertEqual(normalize_url(url), expected)

    def test_lowercase_domain(self):
        url = "HTTP://EXAMPLE.COM/Path"
        expected = "http://example.com/Path"
        self.assertEqual(normalize_url(url), expected)
        
    def test_empty_url(self):
        self.assertEqual(normalize_url(""), "")

if __name__ == '__main__':
    unittest.main()
