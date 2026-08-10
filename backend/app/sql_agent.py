"""
SQL Agent
"""

from backend.app.state import AgentState
from backend.app.services.sql_service import process_sql_query


def sql_agent(state: AgentState) -> AgentState:
    """
    SQL Agent

    Responsible for handling database-related queries.
    """

    print("SQL Agent Executed")

    state["response"] = process_sql_query(state["query"])

    return state
