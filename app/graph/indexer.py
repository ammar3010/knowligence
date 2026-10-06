import logging
from time import perf_counter

from app.graph.extractor import GraphExtractor
from app.graph.repository import GraphRepository
from app.models.documents import DocumentChunk

logger = logging.getLogger(__name__)


class GraphIndexer:

    def __init__(self):
        self.extractor = GraphExtractor()
        self.repository = GraphRepository()

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        if not chunks:
            logger.info("Graph indexing skipped: no chunks supplied")
            return
        started_at = perf_counter()
        logger.info("Graph indexing started: chunks=%d", len(chunks))
        self.repository.create_constraints()

        for chunk in chunks:

            self.repository.store_chunk(
                chunk
            )

            extraction = self.extractor.extract(
                chunk
            )
            logger.debug(
                "Graph chunk extracted: chunk_id=%s entities=%d relationships=%d",
                chunk.id,
                len(extraction.entities),
                len(extraction.relationships),
            )

            self.repository.store_extraction(
                chunk,
                extraction,
            )
        logger.info(
            "Graph indexing completed: chunks=%d duration_ms=%.1f",
            len(chunks),
            (perf_counter() - started_at) * 1000,
        )