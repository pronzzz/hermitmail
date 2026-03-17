from sklearn.cluster import KMeans
from typing import List, Dict, Any
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    pass

from src.summarization.llm_client import LocalLLMClient

class ClusteringEngine:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self._model = None
        self.embedding_model_name = embedding_model
        
    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.embedding_model_name)
        return self._model
        
    def group_articles(self, articles: List[Dict[str, Any]], num_clusters: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups articles based on topic similarity.
        Returns a dictionary mapping generated section headings to lists of articles.
        """
        if not articles:
            return {}
            
        if len(articles) <= 3:
            return {"Updates": articles}
            
        # Determine number of clusters if not provided
        if num_clusters is None:
            num_clusters = max(2, min(len(articles) // 3, 5))
            
        # Extract summaries for embedding
        texts = [article.get('summary', article.get('title', '')) for article in articles]
        
        # Embed
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Cluster
        kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
        labels = kmeans.fit_predict(embeddings)
        
        # Organize by cluster index
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(articles[idx])
            
        # Generate section headings
        llm_client = LocalLLMClient()
        final_groups = {}
        
        for cluster_id, cluster_articles in clusters.items():
            if len(cluster_articles) == 1:
                heading = "Miscellaneous"
            else:
                # Ask LLM for a heading
                titles = [a.get('title', '') for a in cluster_articles]
                prompt = (
                    "You are a newsletter editor. Read these article titles and provide a single 2-4 word section heading that groups them thematically.\n"
                    "Do not add any explanations, quotes, or markdown. Output exactly the heading text and nothing else.\n\n"
                     f"TITLES:\n{chr(10).join(titles)}"
                )
                try:
                    import ollama
                    response = ollama.chat(model=llm_client.model, messages=[
                        {'role': 'user', 'content': prompt}
                    ])
                    heading = response.get('message', {}).get('content', '').strip().strip('"').strip('*')
                except Exception:
                    heading = f"Section {cluster_id + 1}"
                    
                if not heading or len(heading) > 50:
                     heading = f"Section {cluster_id + 1}"
                     
            final_groups[heading] = cluster_articles
            
        return final_groups
