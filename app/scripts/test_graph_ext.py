from app.graph.extractor import GraphExtractor
from app.ingestion.pipeline import IngestionPipeline


def main():
    pipeline = IngestionPipeline()
    extractor = GraphExtractor()

    document, chunks = pipeline.ingest(
        "D:\\knowligence\\app\\data\\sample.txt"
    )

    print("=" * 60)
    print("GRAPH EXTRACTION")
    print("=" * 60)

    for chunk in chunks:

        result = extractor.extract(chunk)

        print()
        print("CHUNK")
        print("-" * 40)
        print(chunk.content)

        print()
        print("ENTITIES")
        print("-" * 40)

        for entity in result.entities:
            print(
                f"{entity.name} "
                f"[{entity.type}]"
            )

        print()
        print("RELATIONSHIPS")
        print("-" * 40)

        for relationship in result.relationships:
            print(
                f"{relationship.source} "
                f"--[{relationship.relation}]--> "
                f"{relationship.target}"
            )


if __name__ == "__main__":
    main()