from app.ingestion.pipeline import IngestionPipeline
from app.vectorstore.repository import VectorRepository


def main():
    pipeline = IngestionPipeline()
    repository = VectorRepository()

    document, chunks = pipeline.ingest(
        "D:\\knowligence\\app\\data\\sample.txt"
    )

    print("=" * 60)
    print("INDEXING")
    print("=" * 60)

    print("Document:", document.title)
    print("Chunks:", len(chunks))

    repository.index_chunks(chunks)

    print("Indexed successfully.")

    print()
    print("=" * 60)
    print("SEARCH")
    print("=" * 60)

    query = "Which company invested in an AI company?"

    results = repository.search(
        query,
        limit=3,
    )

    print("Query:", query)
    print()

    for index, result in enumerate(results, start=1):
        print(f"Result {index}")
        print("Score:", result.score)
        print("Content:")
        print(result.payload["content"])
        print("-" * 40)


if __name__ == "__main__":
    main()