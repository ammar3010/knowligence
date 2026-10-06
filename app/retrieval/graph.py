from app.graph.client import neo4j_client


class GraphRetriever:
    def retrieve_entities(self, entity_names: list[str]):
        if not entity_names:
            return []

        query = """
        MATCH (e:Entity)
        WHERE e.name IN $entity_names
        RETURN e.name AS name,
               e.type AS type,
               e.description AS description
        """

        return neo4j_client.execute(
            query,
            {"entity_names": entity_names},
        )

    def retrieve_relationships(
        self,
        entity_names: list[str],
        max_hops: int = 2,
    ):
        if not entity_names:
            return []

        max_hops = max(1, min(max_hops, 4))

        query = f"""
        MATCH path = (start:Entity)-[:RELATES_TO*1..{max_hops}]->(end:Entity)
        WHERE start.name IN $entity_names

        RETURN [
            node IN nodes(path) |
            {{
                name: node.name,
                type: node.type,
                description: node.description
            }}
        ] AS entities,

        [
            relationship IN relationships(path) |
            {{
                relation: relationship.relation,
                description: relationship.description
            }}
        ] AS relationships
        """

        return neo4j_client.execute(
            query,
            {"entity_names": entity_names},
        )

    def retrieve_facts(self, entity_names: list[str]):
        if not entity_names:
            return []

        query = """
        MATCH (f:Fact)-[:SUBJECT]->(source:Entity),
              (f)-[:OBJECT]->(target:Entity),
              (c:Chunk)-[:SUPPORTS]->(f)
        WHERE source.name IN $entity_names
           OR target.name IN $entity_names
        RETURN
            source.name AS source,
            source.type AS source_type,
            f.relation AS relation,
            target.name AS target,
            target.type AS target_type,
            f.description AS description,
            c.id AS chunk_id,
            c.document_id AS document_id,
            c.content AS content,
            c.source AS source_document
        """

        return neo4j_client.execute(
            query,
            {"entity_names": entity_names},
        )