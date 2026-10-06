from typing import Any, TypedDict


class GraphRAGState(TypedDict, total=False):
    query: str
    entities: list[str]

    vector_results: list[Any]
    graph_relationships: list[Any]
    graph_facts: list[Any]

    context: str
    answer: str

    sources: list[dict]
    graph_paths: list[dict]