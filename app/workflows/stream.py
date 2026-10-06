from app.llm.groq import groq_client
from app.llm.prompts import ANSWER_PROMPT
from app.retrieval.context import build_context
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.response import (
    build_graph_paths,
    build_sources,
)


retriever = HybridRetriever()


def stream_query(
    query: str,
    chat_history,
):
    result = retriever.retrieve(
        query=query,
        top_k=5,
        max_hops=2,
    )

    state = {
        "query": query,
        "chat_history": chat_history,
        "entities": result["entity_names"],
        "vector_results": result["vector_results"],
        "graph_relationships": result["graph_relationships"],
        "graph_facts": result["graph_facts"],
    }

    context = build_context(state)

    formatted_history = "\n".join(
        f"{message.role.upper()}: {message.content}"
        for message in chat_history
    )

    if not formatted_history:
        formatted_history = "No previous conversation."

    prompt = ANSWER_PROMPT.format(
        query=query,
        chat_history=formatted_history,
        context=context,
    )

    answer_parts = []

    for token in groq_client.stream_answer(prompt):
        answer_parts.append(token)
        yield {
            "type": "token",
            "content": token,
        }

    state["answer"] = "".join(answer_parts)
    state["sources"] = build_sources(state)
    state["graph_paths"] = build_graph_paths(state)

    yield {
        "type": "done",
        "entities": state["entities"],
        "sources": state["sources"],
        "graph_paths": state["graph_paths"],
    }