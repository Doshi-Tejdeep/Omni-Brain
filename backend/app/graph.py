from langgraph.graph import StateGraph, START, END

from state import AgentState
from router import route_query
from search_agent import search_agent

# Create a new workflow
workflow = StateGraph(AgentState)

# Add the Supervisor node
workflow.add_node("supervisor", route_query)

#search agent node
workflow.add_node("search_agent", search_agent)

# Define the workflow
workflow.add_edge(START, "supervisor")
workflow.add_edge("supervisor", "search_agent")
workflow.add_edge("search_agent", END)

# Compile the graph
graph = workflow.compile()