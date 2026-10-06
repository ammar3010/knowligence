from typing import Any, TypedDict

from app.models.response import ChatMessage


class GraphRAGState(TypedDict, total=False):
    query: str
    chat_history: list[ChatMessage]

    entities: list[str]

    vector_results: list[Any]
    graph_relationships: list[Any]
    graph_facts: list[Any]

    context: str
    answer: str

    sources: list[dict]
    graph_paths: list[dict]