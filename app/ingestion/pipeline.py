from app.ingestion.factory import DocumentLoaderFactory
from app.ingestion.chunker import DocumentChunker
from app.models.documents import Document, DocumentChunk


class IngestionPipeline:

    def __init__(self):
        self.chunker = DocumentChunker()

    def load(self, source: str) -> Document:
        loader = DocumentLoaderFactory.get_loader(source)

        document = loader.load(source)

        if not document.content.strip():
            raise ValueError(
                f"No usable content found in: {source}"
            )

        return document

    def ingest(
        self,
        source: str,
    ) -> tuple[Document, list[DocumentChunk]]:

        document = self.load(source)

        chunks = self.chunker.chunk(document)

        return document, chunks