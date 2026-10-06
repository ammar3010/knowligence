from langgraph.graph import END, START, StateGraph

from app.workflows.nodes import (
    context_node,
    reasoning_node,
    response_node,
    retrieve_node,
)
from app.workflows.state import GraphRAGState


def build_graph():
    workflow = StateGraph(GraphRAGState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("context", context_node)
    workflow.add_node("reason", reasoning_node)
    workflow.add_node("response", response_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "context")
    workflow.add_edge("context", "reason")
    workflow.add_edge("reason", "response")
    workflow.add_edge("response", END)

    return workflow.compile()


graph = build_graph()