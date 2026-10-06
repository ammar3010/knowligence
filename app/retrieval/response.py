from app.models.response import GraphPath, Source
from app.workflows.state import GraphRAGState


def build_sources(state: GraphRAGState) -> list[dict]:
    sources = []
    seen = set()

    # Graph facts are strongest because they represent
    # explicit relationships with source provenance.
    for fact in state.get("graph_facts", []):
        chunk_id = fact.get("chunk_id")

        if not chunk_id or chunk_id in seen:
            continue

        seen.add(chunk_id)

        sources.append(
            {
                "chunk_id": chunk_id,
                "document_id": fact.get("document_id"),
                "document": fact.get("source_document"),
                "content": fact.get("content", ""),
                "score": None,
            }
        )

    # Add vector results that are not already represented.
    for result in state.get("vector_results", []):
        payload = result.payload or {}
        chunk_id = payload.get("chunk_id")

        if not chunk_id or chunk_id in seen:
            continue

        seen.add(chunk_id)

        sources.append(
            {
                "chunk_id": chunk_id,
                "document_id": payload.get("document_id"),
                "document": payload.get("source"),
                "content": payload.get("content", ""),
                "score": result.score,
            }
        )

    return sources


def build_graph_paths(state: GraphRAGState) -> list[dict]:
    paths = []
    seen = set()

    for fact in state.get("graph_facts", []):
        source = fact.get("source")
        relation = fact.get("relation")
        target = fact.get("target")

        if not source or not relation or not target:
            continue

        key = (source, relation, target)

        if key in seen:
            continue

        seen.add(key)

        paths.append(
            {
                "source": source,
                "relationship": relation,
                "target": target,
                "description": fact.get("description"),
            }
        )

    return paths