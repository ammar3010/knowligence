from app.embedding.model import get_embedding_model
from app.models.documents import DocumentChunk
from app.vectorstore.client import qdrant_client


class VectorRepository:

    def __init__(self):
        self.embeddings = get_embedding_model()

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:

        if not chunks:
            return

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

    def search(
        self,
        query: str,
        limit: int = 8,
    ):

        embedding = self.embeddings.embed_text(query)

        return qdrant_client.search(
            embedding,
            limit=limit,
        )