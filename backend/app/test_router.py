from router import route_query

test_queries = [
    "Show employee database",
    "Display sales chart",
    "Explain the uploaded document"
]

for query in test_queries:
    state = {
        "query": query,
        "route": "",
        "context": "",
        "response": ""
    }

    result = route_query(state)
    print(f"Query: {query}")
    print(f"Selected Route: {result['route']}")
    print("-" * 40)