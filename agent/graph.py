from langgraph.graph import StateGraph
from rag.retriever import retrieve
from rag.llm_rag import generate_response
from utils.parser import split_clauses


# Extract clauses
def extract_clauses(state):
    text = state["text"]

    clauses = split_clauses(text)

    print("CLAUSES FOUND:", len(clauses))  # debug

    return {
        "text": text,
        "clauses": clauses,
        "current_index": 0,
        "results": []
    }


# Analyze clause
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


# Move next
def next_clause(state):
    state["current_index"] += 1
    return state


# Condition
def has_more_clauses(state):
    return state["current_index"] < len(state["clauses"])


# Report
def generate_report(state):
    report = "\n📄 CONTRACT RISK REPORT\n\n"

    for r in state["results"]:
        report += f"Clause:\n{r['clause']}\n\n"
        report += f"{r['analysis']}\n"
        report += "-" * 50 + "\n"

    state["report"] = report
    return state


# Build graph
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