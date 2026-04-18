import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load dataset
df = pd.read_csv("Data/legal_contract_clauses.csv")

clauses = df["clause_text"].tolist()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(clauses)

# Persistent database
client = chromadb.Client(
    Settings(
        persist_directory="./chroma_db",
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection("legal_clauses")

# Clear old data (important while developing)
collection.delete(where={})

for i, clause in enumerate(clauses):
    collection.add(
        ids=[str(i)],
        documents=[clause],
        embeddings=[embeddings[i].tolist()]
    )

print(f"Stored {len(clauses)} clauses in vector database.")