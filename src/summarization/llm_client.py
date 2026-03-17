import ollama

class LocalLLMClient:
    def __init__(self, model: str = "llama3:8b", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        # The ollama package by default expects the daemon to be at localhost:11434.
        
    def summarize_article(self, title: str, text: str) -> str:
        """
        Creates a strict 2-sentence summary of the article without hallucinations.
        Ensures the article title is cited.
        """
        prompt = f"""
        You are a neutral summarizer. Given the article text below, provide exactly a 2-sentence summary.
        You must cite the article's title ("{title}") in your summary.
        Do not add external knowledge, speculate, or editorialize. Extract facts only.
        
        ARTICLE TITLE: {title}
        ARTICLE TEXT:
        {text[:8000]}  # limit context to prevent OOM
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            summary = response.get('message', {}).get('content', '').strip()
            return summary
        except Exception as e:
            # Handle model not found or connection error
            return f"Error connecting to local LLM: {str(e)}"
