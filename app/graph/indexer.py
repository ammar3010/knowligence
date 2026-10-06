from app.graph.extractor import GraphExtractor
from app.graph.repository import GraphRepository
from app.models.documents import Document, DocumentChunk


class GraphIndexer:
    def __init__(self):
        self.extractor = GraphExtractor()
        self.repository = GraphRepository()

    def index_document(
        self,
        document: Document,
        chunks: list[DocumentChunk],
    ) -> None:
        self.repository.create_constraints()
        self.repository.store_document(document)

        for chunk in chunks:
            self.repository.store_chunk(chunk)

            extraction = self.extractor.extract(chunk)

            self.repository.store_extraction(
                chunk,
                extraction,
            )