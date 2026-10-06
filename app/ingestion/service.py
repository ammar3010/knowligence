import tempfile
from pathlib import Path

from app.graph.indexer import GraphIndexer
from app.ingestion.chunker import DocumentChunker
from app.ingestion.loader import get_loader
from app.models.documents import Document, DocumentChunk, DocumentType
from app.vectorstore.repository import VectorRepository


class IngestionService:
    def __init__(self):
        self.vector_repository = VectorRepository()
        self.graph_indexer = GraphIndexer()
        self.chunker = DocumentChunker()

    def load_and_chunk_file(
        self,
        content: bytes,
        filename: str,
        document_id: str,
        document_type: DocumentType,
    ) -> tuple[Document, list[DocumentChunk]]:

        suffix = Path(filename).suffix.lower()

        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=True,
        ) as temp_file:

            temp_file.write(content)
            temp_file.flush()

            loader = get_loader(document_type)
            document = loader.load(temp_file.name)

        document = document.model_copy(
            update={
                "id": document_id,
                "source": filename,
                "metadata": {
                    **document.metadata,
                    "filename": filename,
                },
            }
        )

        chunks = self.chunker.chunk(document)

        return document, chunks

    def ingest(
        self,
        document: Document,
        chunks: list[DocumentChunk],
    ) -> int:

        self.vector_repository.index_chunks(chunks)

        self.graph_indexer.index_document(
            document,
            chunks,
        )

        return len(chunks)