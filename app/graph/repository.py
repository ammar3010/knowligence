from app.graph.client import neo4j_client
from app.models.documents import DocumentChunk
from app.models.graph import GraphExtraction


class GraphRepository:

    def create_constraints(self) -> None:
        neo4j_client.execute(
            """
            CREATE CONSTRAINT entity_name_unique IF NOT EXISTS
            FOR (e:Entity)
            REQUIRE e.name IS UNIQUE
            """
        )

        neo4j_client.execute(
            """
            CREATE CONSTRAINT chunk_id_unique IF NOT EXISTS
            FOR (c:Chunk)
            REQUIRE c.id IS UNIQUE
            """
        )

    def store_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:

        neo4j_client.execute(
            """
            MERGE (c:Chunk {id: $chunk_id})
            SET
                c.content = $content,
                c.document_id = $document_id,
                c.chunk_index = $chunk_index,
                c.token_count = $token_count,
                c.source = $source,
                c.title = $title
            """,
            {
                "chunk_id": chunk.id,
                "content": chunk.content,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "token_count": chunk.token_count,
                "source": chunk.metadata.get("source"),
                "title": chunk.metadata.get("title"),
            },
        )

    def store_extraction(
        self,
        chunk: DocumentChunk,
        extraction: GraphExtraction,
    ) -> None:

        # Store entities and their connection to the source chunk.
        for entity in extraction.entities:

            neo4j_client.execute(
                """
                MERGE (e:Entity {name: $name})
                SET
                    e.type = $type,
                    e.description = $description

                WITH e

                MATCH (c:Chunk {id: $chunk_id})

                MERGE (c)-[:MENTIONS]->(e)
                """,
                {
                    "name": entity.name,
                    "type": entity.type,
                    "description": entity.description,
                    "chunk_id": chunk.id,
                },
            )

        # Store relationships between entities.
        for relationship in extraction.relationships:

            neo4j_client.execute(
                """
                MERGE (source:Entity {name: $source})
                SET source.type = $source_type

                MERGE (target:Entity {name: $target})
                SET target.type = $target_type

                MERGE (source)-[r:RELATES_TO {
                    relation: $relation
                }]->(target)

                SET r.description = $description

                WITH source, target

                MATCH (c:Chunk {id: $chunk_id})

                MERGE (f:Fact {
                    chunk_id: $chunk_id,
                    source: $source,
                    relation: $relation,
                    target: $target
                })

                SET
                    f.description = $description

                MERGE (c)-[:SUPPORTS]->(f)
                MERGE (f)-[:SUBJECT]->(source)
                MERGE (f)-[:OBJECT]->(target)
                """,
                {
                    "source": relationship.source,
                    "source_type": relationship.source_type,
                    "target": relationship.target,
                    "target_type": relationship.target_type,
                    "relation": relationship.relation,
                    "description": relationship.description,
                    "chunk_id": chunk.id,
                },
            )