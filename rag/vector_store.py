import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

# Load dataset
df = pd.read_csv("Data/legal_contract_clauses.csv")

print(df.columns)

# Correct column name
clauses = df["clause_text"].tolist()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(clauses)

# Initialize ChromaDB
client = chromadb.Client()

collection = client.create_collection("legal_clauses")

for i, clause in enumerate(clauses):
    collection.add(
        documents=[clause],
        embeddings=[embeddings[i].tolist()],
        ids=[str(i)]
    )

print("Vector database created successfully!")