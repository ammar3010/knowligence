from app.workflows.graph import graph
import json

def main():
    query = "What relationships does Microsoft have with OpenAI?"

    result = graph.invoke(
        {
            "query": query,
        }
    )

    print("\n" + "=" * 60)
    print("ASSEMBLED CONTEXT")
    print("=" * 60)
    print(result["context"])

    print("=" * 60)
    print("LANGGRAPH RETRIEVAL WORKFLOW")
    print("=" * 60)

    print("\nQUERY:")
    print(result["query"])

    print("\nENTITIES:")
    print(result["entities"])

    print("\nVECTOR RESULTS:")
    for item in result["vector_results"]:
        print(item.payload.get("content"))

    print("\nGRAPH RELATIONSHIPS:")
    for item in result["graph_relationships"]:
        print(item)

    print("\nGRAPH FACTS:")
    for item in result["graph_facts"]:
        print(item)

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(result["answer"])

    print("\n" + "=" * 60)
    print("STRUCTURED RESPONSE")
    print("=" * 60)

    response = {
        "answer": result["answer"],
        "entities": result["entities"],
        "sources": result["sources"],
        "graph_paths": result["graph_paths"],
    }

    print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()