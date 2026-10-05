from app.ingestion.pipeline import IngestionPipeline


def main():
    pipeline = IngestionPipeline()

    document, chunks = pipeline.ingest(
        "D:\\knowligence\\app\\data\\sample.txt"
    )

    print("=" * 60)
    print("DOCUMENT")
    print("=" * 60)

    print("ID:", document.id)
    print("Title:", document.title)
    print("Source:", document.source)
    print("Type:", document.source_type)
    print("Characters:", len(document.content))

    print()
    print("=" * 60)
    print(f"CHUNKS ({len(chunks)})")
    print("=" * 60)

    for chunk in chunks:
        print()
        print(f"Chunk: {chunk.chunk_index}")
        print(f"ID: {chunk.id}")
        print(f"Tokens: {chunk.token_count}")
        print("-" * 40)
        print(chunk.content)


if __name__ == "__main__":
    main()