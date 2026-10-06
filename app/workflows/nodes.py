from app.retrieval.hybrid import HybridRetriever
from app.llm.groq import groq_client
from app.workflows.state import GraphRAGState
from app.llm.prompts import ANSWER_PROMPT
from app.retrieval.context import build_context
from app.retrieval.response import build_graph_paths, build_sources

retriever = HybridRetriever()


def retrieve_node(state: GraphRAGState) -> GraphRAGState:
    result = retriever.retrieve(
        query=state["query"],
        top_k=5,
        max_hops=2,
    )

    return {
        **state,
        "entities": result["entity_names"],
        "vector_results": result["vector_results"],
        "graph_relationships": result["graph_relationships"],
        "graph_facts": result["graph_facts"],
    }

def context_node(state: GraphRAGState) -> GraphRAGState:
    context = build_context(state)

    return {
        **state,
        "context": context,
    }

def reasoning_node(state: GraphRAGState) -> GraphRAGState:
    prompt = ANSWER_PROMPT.format(
        query=state["query"],
        context=state["context"],
    )

    answer = groq_client.generate_answer(prompt)

    return {
        **state,
        "answer": answer,
    }

def response_node(state: GraphRAGState) -> GraphRAGState:
    return {
        **state,
        "sources": build_sources(state),
        "graph_paths": build_graph_paths(state),
    }