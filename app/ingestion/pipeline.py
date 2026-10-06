import logging
from pathlib import Path

from app.ingestion.factory import DocumentLoaderFactory
from app.ingestion.chunker import DocumentChunker
from app.models.documents import Document, DocumentChunk

logger = logging.getLogger(__name__)


class IngestionPipeline:

    def __init__(self):
        self.chunker = DocumentChunker()

    def load(self, source: str) -> Document:
        source_type = "web" if source.startswith(("http://", "https://")) else Path(source).suffix.lower()
        logger.info("Document loading started: source_type=%s", source_type or "unknown")
        loader = DocumentLoaderFactory.get_loader(source)

        try:
            document = loader.load(source)
        except Exception:
            logger.exception("Document loading failed: source_type=%s", source_type or "unknown")
            raise

        if not document.content.strip():
            logger.warning("Document contains no usable text: document_id=%s", document.id)
            raise ValueError(
                f"No usable content found in: {source}"
            )

        logger.info(
            "Document loaded: document_id=%s source_type=%s content_chars=%d",
            document.id,
            document.source_type.value,
            len(document.content),
        )
        return document

    def ingest(
        self,
        source: str,
    ) -> tuple[Document, list[DocumentChunk]]:

        document = self.load(source)

        chunks = self.chunker.chunk(document)
        logger.info("Document chunking completed: document_id=%s chunks=%d", document.id, len(chunks))

        return document, chunks