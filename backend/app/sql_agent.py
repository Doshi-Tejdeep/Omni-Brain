from state import AgentState

def sql_agent(state: AgentState) -> AgentState:
    """
    SQL Agent

    Responsible for handling database-related queries.
    """

    print("SQL Agent Executed")

    state["response"] = "SQL Agent processed the query."

    return state