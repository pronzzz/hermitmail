import unittest
from unittest.mock import patch
from src.clustering.grouper import ClusteringEngine

class TestClustering(unittest.TestCase):
    @patch('src.clustering.grouper.LocalLLMClient')
    def test_group_articles(self, mock_llm_client):
        # We need realistic enough embeddings to test kmeans without actually running sentence-transformers
        # We will mock the model's encode method
        
        class MockModel:
            def encode(self, texts, convert_to_numpy=True):
                import numpy as np
                # Return distinct vectors for distinct groups
                # Group 1: animals (idx 0, 1)
                # Group 2: tech (idx 2, 3)
                embeddings = []
                for t in texts:
                    if "cat" in t.lower() or "dog" in t.lower():
                        embeddings.append([1.0, 0.0, 0.0])
                    else:
                        embeddings.append([0.0, 1.0, 0.0])
                return np.array(embeddings)
                
        engine = ClusteringEngine()
        engine._model = MockModel() # Inject mock model
        
        # Mock LLM Client
        mock_instance = mock_llm_client.return_value
        
        # We can't easily patch ollama.chat directly since we're inside the method,
        # but we can patch it globally or let the exception handler fallback to "Section X"
        # Since we just want to test grouping, the fallback is fine.
        
        articles = [
            {"title": "Cats are great", "summary": "Cat"},
            {"title": "Dogs are great", "summary": "Dog"},
            {"title": "New iPhone", "summary": "Tech phone"},
            {"title": "Macbook Pro", "summary": "Tech laptop"},
        ]
        
        groups = engine.group_articles(articles, num_clusters=2)
        
        self.assertEqual(len(groups), 2)
        
        # Verify sizes (2 items per group due to mock embedding logic)
        sizes = [len(v) for v in groups.values()]
        sizes.sort()
        self.assertEqual(sizes, [2, 2])

    def test_few_articles(self):
        engine = ClusteringEngine()
        articles = [{"title": "One"}]
        groups = engine.group_articles(articles)
        self.assertEqual(list(groups.keys()), ["Updates"])
        self.assertEqual(len(groups["Updates"]), 1)

if __name__ == '__main__':
    unittest.main()
