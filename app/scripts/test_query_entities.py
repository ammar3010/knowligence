from app.retrieval.query import QueryEntityExtractor


def main():
    extractor = QueryEntityExtractor()

    queries = [
        "What is Microsoft's relationship with OpenAI?",
        "How does Google compete with Microsoft?",
        "What companies operate cloud platforms?",
    ]

    for query in queries:
        entities = extractor.extract(query)

        print("=" * 60)
        print("QUERY:", query)
        print("ENTITIES:", entities)


if __name__ == "__main__":
    main()