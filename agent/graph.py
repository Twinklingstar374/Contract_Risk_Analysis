from langgraph.graph import StateGraph
from rag.retriever import retrieve
from rag.llm_rag import generate_response


# 🧠 1️⃣ Extract clauses
def extract_clauses(state):
    text = state["text"]

    clauses = text.split(".")
    clauses = [c.strip() for c in clauses if len(c.strip()) > 20]

    return {
        "clauses": clauses,
        "current_index": 0,
        "results": []
    }


# 🔍 2️⃣ Analyze clause (RAG + LLM)
def analyze_clause(state):
    idx = state["current_index"]
    clause = state["clauses"][idx]

    docs = retrieve(clause)
    response = generate_response(clause, docs)

    state["results"].append({
        "clause": clause,
        "analysis": response
    })

    return state


# 🔁 3️⃣ Move to next clause
def next_clause(state):
    state["current_index"] += 1
    return state


# ❓ 4️⃣ Check condition
def has_more_clauses(state):
    return state["current_index"] < len(state["clauses"])


# Generate final report
def generate_report(state):
    report = "\n📄 CONTRACT RISK REPORT\n\n"

    for r in state["results"]:
        report += f"Clause: {r['clause']}\n"
        report += f"{r['analysis']}\n"
        report += "-" * 50 + "\n"

    state["report"] = report
    return state


#  BUILD GRAPH
def build_agent():
    graph = StateGraph(dict)

    graph.add_node("extract", extract_clauses)
    graph.add_node("analyze", analyze_clause)
    graph.add_node("next", next_clause)
    graph.add_node("report", generate_report)

    graph.set_entry_point("extract")

    graph.add_edge("extract", "analyze")
    graph.add_edge("analyze", "next")

    graph.add_conditional_edges(
        "next",
        has_more_clauses,
        {
            True: "analyze",
            False: "report"
        }
    )

    return graph.compile()