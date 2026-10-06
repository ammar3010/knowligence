from app.workflows.state import GraphRAGState


def build_context(state: GraphRAGState) -> str:
    sections = []

    # Vector evidence
    vector_results = state.get("vector_results", [])

    if vector_results:
        sections.append("VECTOR EVIDENCE")

        for index, result in enumerate(vector_results, start=1):
            payload = result.payload or {}

            sections.append(
                f"""
[Vector Result {index}]
Score: {result.score}
Source: {payload.get("source")}
Content:
{payload.get("content")}
""".strip()
            )

    # Graph relationships
    graph_relationships = state.get("graph_relationships", [])

    if graph_relationships:
        sections.append("GRAPH RELATIONSHIPS")

        for index, item in enumerate(graph_relationships, start=1):
            sections.append(
                f"""
[Graph Path {index}]
Entities: {item.get("entities")}
Relationships: {item.get("relationships")}
""".strip()
            )

    # Graph facts
    graph_facts = state.get("graph_facts", [])

    if graph_facts:
        sections.append("GRAPH FACTS")

        for index, fact in enumerate(graph_facts, start=1):
            sections.append(
                f"""
[Graph Fact {index}]
{fact.get("source")} --{fact.get("relation")}--> {fact.get("target")}
Description: {fact.get("description")}
Source: {fact.get("source_document")}
Chunk ID: {fact.get("chunk_id")}
Evidence:
{fact.get("content")}
""".strip()
            )

    return "\n\n".join(sections)