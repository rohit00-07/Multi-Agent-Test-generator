from langgraph.graph import StateGraph
from core.state import OrchestratorState
from orchestrator.nodes import generate_node, validate_node, store_node

def build_graph():
    graph = StateGraph(OrchestratorState)

    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("store", store_node)

    graph.set_entry_point("generate")

    graph.add_edge("generate", "validate")

    graph.add_conditional_edges(
        "validate",
        lambda state: "store" if state.is_valid else "generate"
    )

    graph.add_conditional_edges(
        "store",
        lambda state: "__end__"
        if len(state.collected_questions) >= state.required_count
        or state.attempts >= state.max_attempts
        else "generate"
    )

    return graph.compile()