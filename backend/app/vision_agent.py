from state import AgentState

def vision_agent(state: AgentState) -> AgentState:
    """
    Vision Agent

    Responsible for handling image and chart-related queries.
    """

    print("Vision Agent Executed")

    state["response"] = "Vision Agent processed the query."

    return state