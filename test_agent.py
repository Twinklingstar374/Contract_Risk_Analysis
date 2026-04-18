from agent.graph import build_agent

agent = build_agent()

contract_text = """
The company shall not be liable for any damages.
The distributor must only sell company products.
Either party may terminate the agreement with 30 days notice.
"""

result = agent.invoke({"text": contract_text})

print(result["report"])