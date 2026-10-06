from pydantic import BaseModel, Field


class Source(BaseModel):
    chunk_id: str
    document_id: str
    document: str | None = None
    content: str
    score: float | None = None


class GraphPath(BaseModel):
    source: str
    relationship: str
    target: str
    description: str | None = None


class GraphRAGResponse(BaseModel):
    answer: str
    entities: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    graph_paths: list[GraphPath] = Field(default_factory=list)