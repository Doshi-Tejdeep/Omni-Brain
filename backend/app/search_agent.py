from state import AgentState

def search_agent(state: AgentState) -> AgentState:
    """
    Search Agent

    Responsible for semantic search and document retrieval.
    """

    print("Search Agent Executed")

    state["response"] = "Search Agent processed the query."

    return state