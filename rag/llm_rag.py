from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(user_clause, retrieved_docs):
    # Build context
    context = ""
    for doc in retrieved_docs:
        context += f"- [{doc['risk']}] {doc['clause']}\n"

    prompt = f"""
You are a legal contract risk analyzer.

Below are similar clauses with known risk levels:

{context}

Now analyze this clause:

"{user_clause}"

Respond EXACTLY in this format:

RISK_LEVEL: High / Medium / Low
REASON: 1-2 sentence explanation
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content