import logging

from app.embedding.model import get_embedding_model
from app.models.documents import DocumentChunk
from app.vectorstore.client import qdrant_client

logger = logging.getLogger(__name__)


class VectorRepository:

    def __init__(self):
        self.embeddings = get_embedding_model()

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:

        if not chunks:
            logger.info("Vector indexing skipped: no chunks supplied")
            return

        logger.info("Vector indexing started: chunks=%d", len(chunks))
        embeddings = self.embeddings.embed_texts(
            [chunk.content for chunk in chunks]
        )

        qdrant_client.create_collection(
            vector_size=self.embeddings.dimension
        )

        qdrant_client.upsert_chunks(
            chunks,
            embeddings,
        )
        logger.info("Vector indexing completed: chunks=%d", len(chunks))

    def search(
        self,
        query: str,
        limit: int = 8,
    ):
        logger.debug("Vector retrieval started: limit=%d", limit)
        embedding = self.embeddings.embed_text(query)
        results = qdrant_client.search(
            embedding,
            limit=limit,
        )
        logger.info("Vector retrieval completed: results=%d", len(results))
        return results