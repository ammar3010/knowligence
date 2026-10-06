import uuid
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings
from app.models.documents import DocumentChunk

logger = logging.getLogger(__name__)


def to_uuid(id_val: str) -> str:
    try:
        return str(uuid.UUID(id_val))
    except (ValueError, AttributeError):
        pass

    if "_" in id_val:
        try:
            return str(uuid.UUID(hex=id_val.split("_", 1)[1]))
        except (ValueError, AttributeError):
            pass

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(id_val)))


class QdrantVectorStore:
    def __init__(self):
        settings = get_settings()

        self.client = QdrantClient(
            url=settings.qdrant_url,
        )

        self.collection_name = settings.qdrant_collection

    def verify_connection(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            logger.exception("Qdrant connectivity check failed")
            return False

    def create_collection(
        self,
        vector_size: int,
    ) -> None:

        try:
            collections = self.client.get_collections()
        except Exception:
            logger.exception("Failed to inspect Qdrant collections")
            raise

        existing = {
            collection.name
            for collection in collections.collections
        }

        if self.collection_name in existing:
            logger.debug("Qdrant collection already exists: collection=%s", self.collection_name)
            return

        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )
        except Exception:
            logger.exception("Failed to create Qdrant collection: collection=%s", self.collection_name)
            raise
        logger.info("Qdrant collection created: collection=%s vector_size=%d", self.collection_name, vector_size)

    def upsert_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):
            points.append(
                PointStruct(
                    id=to_uuid(chunk.id),
                    vector=embedding,
                    payload={
                        "chunk_id": chunk.id,
                        "document_id": chunk.document_id,
                        "content": chunk.content,
                        "chunk_index": chunk.chunk_index,
                        "token_count": chunk.token_count,
                        **chunk.metadata,
                    },
                )
            )

        if points:
            logger.debug("Upserting vectors: collection=%s points=%d", self.collection_name, len(points))
            try:
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points,
                )
            except Exception:
                logger.exception(
                    "Qdrant vector upsert failed: collection=%s points=%d",
                    self.collection_name,
                    len(points),
                )
                raise

    def search(
        self,
        embedding: list[float],
        limit: int = 8,
    ):

        try:
            points = self.client.query_points(
                collection_name=self.collection_name,
                query=embedding,
                limit=limit,
                with_payload=True,
            ).points
        except Exception:
            logger.exception("Qdrant search failed: collection=%s limit=%d", self.collection_name, limit)
            raise
        logger.debug("Qdrant search completed: collection=%s results=%d", self.collection_name, len(points))
        return points

    def close(self) -> None:
        self.client.close()
        logger.info("Qdrant client closed")


qdrant_client = QdrantVectorStore()