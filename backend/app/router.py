from state import AgentState


def route_query(state: AgentState) -> AgentState:
    """
    Simple keyword-based routing.
    This will later be replaced with LangGraph routing.
    """

    query = state["query"].lower()

    if "sql" in query or "table" in query or "database" in query:
        state["route"] = "sql"

    elif "image" in query or "chart" in query or "graph" in query:
        state["route"] = "vision"

    else:
        state["route"] = "search"

    return state