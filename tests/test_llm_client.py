import unittest
from unittest.mock import patch, MagicMock
from src.summarization.llm_client import LocalLLMClient

class TestLLMClient(unittest.TestCase):
    @patch('src.summarization.llm_client.ollama.chat')
    def test_summarize_article(self, mock_chat):
        # Mock successful response
        mock_chat.return_value = {
            'message': {
                'content': 'In "Test Article", researchers found a new element. It was discovered under a volcano.'
            }
        }
        
        client = LocalLLMClient()
        summary = client.summarize_article("Test Article", "Some long text about a volcano...")
        self.assertIn("Test Article", summary)
        self.assertIn("volcano", summary)
        mock_chat.assert_called_once()
        
    @patch('src.summarization.llm_client.ollama.chat')
    def test_summarize_error(self, mock_chat):
        # Mock connection error
        mock_chat.side_effect = Exception("Connection refused")
        
        client = LocalLLMClient()
        summary = client.summarize_article("Failed Article", "Text...")
        self.assertTrue(summary.startswith("Error connecting to local LLM"))

if __name__ == '__main__':
    unittest.main()
