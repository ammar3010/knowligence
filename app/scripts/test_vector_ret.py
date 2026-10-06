from app.retrieval.vector import VectorRetriever


def main():
    retriever = VectorRetriever()

    query = "Which companies are mentioned in the document?"

    results = retriever.retrieve(query, top_k=5)

    print("=" * 60)
    print("VECTOR RETRIEVAL")
    print("=" * 60)
    print("Query:", query)
    print("Results:", len(results))
    print()

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print("Score:", result.score)
        print("Chunk ID:", result.payload.get("chunk_id"))
        print("Content:")
        print(result.payload.get("content"))
        print()


if __name__ == "__main__":
    main()