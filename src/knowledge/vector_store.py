import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    # Use a dummy wrapper if not installed yet during tests, 
    # to avoid failing if they haven't run `pip install sentence-transformers`
    # (Though we'll write the code correctly assuming it exists)
    pass

class VectorStore:
    def __init__(self, index_path: str = "hermitmail.faiss", meta_path: str = "hermitmail_faiss_meta.pkl", embedding_model: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.meta_path = meta_path
        self.dimension = 384  # Default for all-MiniLM-L6-v2
        
        # Load or create index
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = [] # List storing URLs corresponding to vectors
            
        # We assume SentenceTransformer is available
        self._model = None
        self._embedding_model_name = embedding_model

    @property
    def model(self):
        # Lazy load the model to save memory if only querying or reading
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._embedding_model_name)
        return self._model

    def add_embeddings(self, url: str, text: str):
        """
        Embeds full text (or summary), adds to FAISS index, and saves to disk.
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        # Faiss expects 2D float32 array
        embedding = np.array([embedding]).astype('float32')
        
        self.index.add(embedding)
        self.metadata.append(url)
        
        self.save()
        
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Searches the DB for similar texts. Returns list of (url, distance) tuples.
        """
        if self.index.ntotal == 0:
            return []
            
        query_embedding = self.model.encode(query, convert_to_numpy=True)
        query_embedding = np.array([query_embedding]).astype('float32')
        
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))
                
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)
