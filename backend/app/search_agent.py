from state import AgentState
from langchain_config import get_llm


def search_agent(state: AgentState) -> AgentState:
    """
    Search Agent

    Handles user queries using the configured LLM.
    """

    print("Search Agent Executed")

    llm = get_llm()

    response = llm.invoke(state["query"])

    state["response"] = response.content

    return state