from rag.retriever import retrieve
from rag.llm_rag import generate_response

query = input("Enter clause:\n")

docs = retrieve(query)

print("\n🔍 Retrieved:\n")
for d in docs:
    print(d)

print("\n🧠 LLM Analysis:\n")

response = generate_response(query, docs)
print(response)