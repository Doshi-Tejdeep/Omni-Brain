from router import route_query

state = {
    "query": "Show me the sales chart",
    "route": "",
    "context": "",
    "response": "",
}

print(route_query(state))