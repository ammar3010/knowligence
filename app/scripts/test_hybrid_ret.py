from app.retrieval.hybrid import HybridRetriever


def main():
    retriever = HybridRetriever()

    query = "Which companies compete with Microsoft through their cloud platforms?"

    result = retriever.retrieve(
        query=query,
        top_k=5,
        max_hops=2,
    )

    print("=" * 60)
    print("AUTOMATIC HYBRID RETRIEVAL")
    print("=" * 60)

    print("\nQUERY:")
    print(result["query"])

    print("\nDETECTED ENTITIES:")
    print(result["entity_names"])

    print("\nVECTOR RESULTS:")
    for index, item in enumerate(result["vector_results"], start=1):
        print(f"\n--- Result {index} ---")
        print("Score:", item.score)
        print("Content:", item.payload.get("content"))

    print("\nGRAPH RELATIONSHIPS:")
    for relationship in result["graph_relationships"]:
        print(relationship)

    print("\nGRAPH FACTS:")
    for fact in result["graph_facts"]:
        print(fact)


if __name__ == "__main__":
    main()