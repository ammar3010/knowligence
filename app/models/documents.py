from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    PDF = "pdf"
    WEB = "web"
    MARKDOWN = "markdown"
    CSV = "csv"
    TEXT = "text"


class Document(BaseModel):
    id: str
    title: str
    source: str
    source_type: DocumentType
    content: str

    metadata: dict = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DocumentChunk(BaseModel):
    id: str
    document_id: str

    content: str
    chunk_index: int

    metadata: dict = Field(default_factory=dict)

    token_count: int | None = None