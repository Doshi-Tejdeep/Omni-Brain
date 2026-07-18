from state import AgentState

# Keywords used for routing
SQL_KEYWORDS = {"sql", "table", "database", "query"}
VISION_KEYWORDS = {"image", "chart", "graph", "plot", "photo"}


def route_query(state: AgentState) -> AgentState:
    """
    Basic keyword-based routing.
    This is the initial workflow and can later be replaced
    with LangGraph or an LLM-based router.
    """

    query = state["query"].lower()

    if any(keyword in query for keyword in SQL_KEYWORDS):
        state["route"] = "sql"

    elif any(keyword in query for keyword in VISION_KEYWORDS):
        state["route"] = "vision"

    else:
        state["route"] = "search"

    return state
