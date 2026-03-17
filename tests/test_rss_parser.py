import unittest
from src.ingestion.rss_parser import parse_rss_links

class TestRSSParser(unittest.TestCase):
    def test_rss_extraction(self):
        rss_xml = """<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0">
        <channel>
            <title>Sample Feed</title>
            <item>
                <title>First Article</title>
                <link>https://example.com/first</link>
            </item>
            <item>
                <title>Second Article</title>
                <link>https://example.com/second</link>
            </item>
        </channel>
        </rss>
        """
        links = parse_rss_links(rss_xml)
        self.assertEqual(links, ["https://example.com/first", "https://example.com/second"])

    def test_atom_extraction(self):
        atom_xml = """<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <title>Sample Feed</title>
            <entry>
                <title>First Atom Article</title>
                <link href="https://example.com/atom/first"/>
            </entry>
            <entry>
                <title>Second Atom Article</title>
                <link href="https://example.com/atom/second" rel="alternate"/>
            </entry>
        </feed>
        """
        links = parse_rss_links(atom_xml)
        self.assertEqual(links, ["https://example.com/atom/first", "https://example.com/atom/second"])

    def test_malformed_xml(self):
        links = parse_rss_links("<rss><channel><item>no end tag")
        self.assertEqual(links, [])

if __name__ == '__main__':
    unittest.main()
