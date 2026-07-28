from graph import graph

# Initial state
initial_state = {
    "query": "What is Artificial Intelligence?",
    "route": "",
    "context": "",
    "response": ""
}

# Execute the graph
result = graph.invoke(initial_state)

print("\nFinal State:")
print(result)