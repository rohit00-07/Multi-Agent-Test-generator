from orchestrator.graph import build_graph

def run_orchestrator(domain_plan: list, difficulty_plan: list, max_attempts: int):
    graph = build_graph()

    initial_state = {
        "domain_plan": domain_plan,
        "difficulty_plan": difficulty_plan,
        "required_count": len(domain_plan),
        "collected_questions": [],
        "current_mcq": None,
        "is_valid": False,
        "attempts": 0,
        "max_attempts": max_attempts
    }

    final_state = graph.invoke(initial_state)
    return final_state["collected_questions"]