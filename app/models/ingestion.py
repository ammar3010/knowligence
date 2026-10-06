from datetime import datetime, timezone

from pydantic import BaseModel


class IngestResponse(BaseModel):
    document_id: str
    filename: str
    source_type: str
    chunks_indexed: int
    message: str


class DocumentInfo(BaseModel):
    document_id: str
    title: str
    source: str
    source_type: str
    chunk_count: int
    created_at: datetime | None = None