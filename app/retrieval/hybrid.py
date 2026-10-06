from app.retrieval.graph import GraphRetriever
from app.retrieval.query import QueryEntityExtractor
from app.retrieval.vector import VectorRetriever


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

        return {
            "query": query,
            "entity_names": entity_names,
            "vector_results": vector_results,
            "graph_relationships": graph_relationships,
            "graph_facts": graph_facts,
        }