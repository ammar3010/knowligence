from app.vectorstore.repository import VectorRepository


class VectorRetriever:
    def __init__(self):
        self.repository = VectorRepository()

    def retrieve(self, query: str, top_k: int = 8):
        return self.repository.search(query, limit=top_k)