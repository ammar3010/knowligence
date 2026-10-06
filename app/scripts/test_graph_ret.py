from app.retrieval.graph import GraphRetriever


def main():
    retriever = GraphRetriever()

    entity_names = ["Microsoft"]

    print("=" * 60)
    print("GRAPH RETRIEVAL")
    print("=" * 60)

    print("\nEntities:")
    entities = retriever.retrieve_entities(entity_names)

    for entity in entities:
        print(entity)

    print("\nRelationships:")
    relationships = retriever.retrieve_relationships(
        entity_names,
        max_hops=2,
    )

    for relationship in relationships:
        print(relationship)

    print("\nFacts:")
    facts = retriever.retrieve_facts(entity_names)

    for fact in facts:
        print(fact)


if __name__ == "__main__":
    main()