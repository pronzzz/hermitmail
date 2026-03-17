import unittest
import os
import sqlite3
from src.knowledge.metadata_store import MetadataStore
from src.knowledge.vector_store import VectorStore

class TestKnowledgeDB(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_meta.sqlite3"
        self.faiss_path = "test_index.faiss"
        self.pkl_path = "test_meta.pkl"
        
        # Clean up old test files
        for f in [self.db_path, self.faiss_path, self.pkl_path]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        for f in [self.db_path, self.faiss_path, self.pkl_path]:
            if os.path.exists(f):
                os.remove(f)

    def test_metadata_store(self):
        store = MetadataStore(db_path=self.db_path)
        
        # Add new
        added = store.add_article("https://example.com/1", "Title 1", "Summary 1")
        self.assertTrue(added)
        
        # Add duplicate
        added_again = store.add_article("https://example.com/1", "Title 1", "Summary 1")
        self.assertFalse(added_again)
        
        # Fetch
        article = store.get_article("https://example.com/1")
        self.assertIsNotNone(article)
        self.assertEqual(article["title"], "Title 1")
        
        # Fetch non-existent
        self.assertIsNone(store.get_article("https://example.com/none"))

    def test_vector_store(self):
        try:
            import sentence_transformers
        except ImportError:
            self.skipTest("sentence-transformers not installed")
            
        store = VectorStore(index_path=self.faiss_path, meta_path=self.pkl_path)
        store.add_embeddings("https://example.com/apple", "Apples are red fruits.")
        store.add_embeddings("https://example.com/car", "Cars have four wheels.")
        
        # Query
        results = store.search("Tell me about a fruit", k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "https://example.com/apple")

if __name__ == '__main__':
    unittest.main()
