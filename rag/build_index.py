import pandas as pd
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading dataset...")
df = pd.read_csv("data/legal_contract_clauses.csv")

# Use correct columns
texts = df["clause_text"].astype(str).tolist()
labels = df["risk_level"].astype(str).tolist()
types = df["clause_type"].astype(str).tolist()

print("Generating embeddings...")
embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

print("Creating FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

print("Saving index...")
faiss.write_index(index, "rag/faiss.index")

print("Saving metadata...")
with open("rag/metadata.pkl", "wb") as f:
    pickle.dump({
        "texts": texts,
        "labels": labels,
        "types": types
    }, f)

print("✅ Index built successfully!")