from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings
from app.models.documents import DocumentChunk


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
            return False

    def create_collection(
        self,
        vector_size: int,
    ) -> None:

        collections = self.client.get_collections()

        existing = {
            collection.name
            for collection in collections.collections
        }

        if self.collection_name in existing:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

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
                    id=chunk.id,
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
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    def search(
        self,
        embedding: list[float],
        limit: int = 8,
    ):

        return self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=limit,
            with_payload=True,
        ).points


qdrant_client = QdrantVectorStore()