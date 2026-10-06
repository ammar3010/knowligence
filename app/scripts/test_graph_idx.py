from app.graph.indexer import GraphIndexer
from app.ingestion.pipeline import IngestionPipeline


def main():
    pipeline = IngestionPipeline()
    indexer = GraphIndexer()

    document, chunks = pipeline.ingest(
        "D:\\knowligence\\app\\data\\sample.txt"
    )

    print("=" * 60)
    print("GRAPH INDEXING")
    print("=" * 60)

    print("Document:", document.title)
    print("Chunks:", len(chunks))

    indexer.index_chunks(chunks)

    print()
    print("Graph indexed successfully.")


if __name__ == "__main__":
    main()