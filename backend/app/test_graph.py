from graph import graph

# Initial state
initial_state = {
    "query": "Explain the uploaded document",
    "route": "",
    "context": "",
    "response": ""
}

# Execute the graph
result = graph.invoke(initial_state)

print("\nFinal State:")
print(result)