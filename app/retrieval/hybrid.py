import logging
from time import perf_counter

from app.retrieval.graph import GraphRetriever
from app.retrieval.query import QueryEntityExtractor
from app.retrieval.vector import VectorRetriever

logger = logging.getLogger(__name__)


class HybridRetriever:
    def __init__(self):
        self.vector_retriever = VectorRetriever()
        self.graph_retriever = GraphRetriever()
        self.entity_extractor = QueryEntityExtractor()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        max_hops: int = 2,
    ):
        started_at = perf_counter()
        logger.info("Hybrid retrieval started: top_k=%d max_hops=%d", top_k, max_hops)
        # 1. Identify entities mentioned in the query
        entity_names = self.entity_extractor.extract(query)

        # 2. Semantic retrieval
        vector_results = self.vector_retriever.retrieve(
            query,
            top_k=top_k,
        )

        # 3. Graph retrieval
        graph_relationships = self.graph_retriever.retrieve_relationships(
            entity_names,
            max_hops=max_hops,
        )

        graph_facts = self.graph_retriever.retrieve_facts(
            entity_names,
        )

        result = {
            "query": query,
            "entity_names": entity_names,
            "vector_results": vector_results,
            "graph_relationships": graph_relationships,
            "graph_facts": graph_facts,
        }
        logger.info(
            "Hybrid retrieval completed: entities=%d vectors=%d relationships=%d facts=%d duration_ms=%.1f",
            len(entity_names),
            len(vector_results),
            len(graph_relationships),
            len(graph_facts),
            (perf_counter() - started_at) * 1000,
        )
        return result