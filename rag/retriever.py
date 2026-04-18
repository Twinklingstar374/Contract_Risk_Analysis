import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading FAISS index...")
index = faiss.read_index("rag/faiss.index")

print("Loading metadata...")
with open("rag/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

texts = metadata["texts"]
labels = metadata["labels"]
types = metadata["types"]


def retrieve(query, k=3):
    query_vec = model.encode([query]).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        results.append({
            "clause": texts[idx],
            "risk": labels[idx],
            "type": types[idx]
        })

    return results