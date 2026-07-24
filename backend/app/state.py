from typing import TypedDict, Literal


class AgentState(TypedDict):
    query: str
    route: Literal["search", "sql", "vision", ""]
    context: str
    response: str
