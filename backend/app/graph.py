from langgraph.graph import StateGraph, START, END

from state import AgentState
from router import route_query, decide_next_node
from search_agent import search_agent
from sql_agent import sql_agent
from vision_agent import vision_agent

# Create a new workflow
workflow = StateGraph(AgentState)

# Add the Supervisor node
workflow.add_node("supervisor", route_query)

#search agent node
workflow.add_node("search_agent", search_agent)
workflow.add_node("sql_agent", sql_agent)
workflow.add_node("vision_agent", vision_agent)

# Define the workflow
workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    decide_next_node,
    {
        "search": "search_agent",
        "sql": "sql_agent",
        "vision": "vision_agent",
    },
)
workflow.add_edge("search_agent", END)
workflow.add_edge("sql_agent", END)
workflow.add_edge("vision_agent", END)


# Compile the graph
graph = workflow.compile()