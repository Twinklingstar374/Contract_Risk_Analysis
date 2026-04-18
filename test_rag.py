from rag.retriever import retrieve

query = input("Enter a contract clause:\n")

results = retrieve(query)

print("\n🔍 Top similar clauses:\n")

for r in results:
    print(f"Clause: {r['clause']}")
    print(f"Type: {r['type']}")
    print(f"Risk: {r['risk']}")
    print("-" * 50)