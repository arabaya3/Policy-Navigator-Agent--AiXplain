import numpy as np
from typing import List
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
class VectorIndex:
    def __init__(self):
        self.docs = []
        self.embeddings = []
    def add_document(self, doc: str, embedding: list):
        self.docs.append(doc)
        self.embeddings.append(embedding)
    def query(self, text: str, embedding: list, top_k=2) -> List[str]:
        if not self.docs:
            return []
        sims = [cosine_similarity(embedding, e) for e in self.embeddings]
        top_indices = np.argsort(sims)[-top_k:][::-1]
        return [self.docs[i] for i in top_indices] 