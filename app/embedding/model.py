import logging
from time import perf_counter

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingModel:
    def __init__(self):
        settings = get_settings()

        started_at = perf_counter()
        logger.info("Loading embedding model: model=%s", settings.embedding_model)
        self.model = SentenceTransformer(
            settings.embedding_model
        )
        logger.info(
            "Embedding model loaded: model=%s duration_ms=%.1f",
            settings.embedding_model,
            (perf_counter() - started_at) * 1000,
        )

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        logger.debug("Embedding text batch: items=%d", len(texts))
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        if hasattr(self.model, "get_embedding_dimension"):
            return self.model.get_embedding_dimension()
        return self.model.get_sentence_embedding_dimension()


@lru_cache
def get_embedding_model() -> EmbeddingModel:
    return EmbeddingModel()