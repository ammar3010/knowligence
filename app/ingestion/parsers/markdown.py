from pathlib import Path

from app.ingestion.loader import BaseDocumentLoader
from app.models.documents import Document, DocumentType
from app.utilities.ids import generate_id


class MarkdownDocumentLoader(BaseDocumentLoader):

    def load(self, source: str) -> Document:
        path = Path(source)

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return Document(
            id=generate_id("doc"),
            title=path.stem,
            source=str(path.absolute()),
            source_type=DocumentType.MARKDOWN,
            content=content,
            metadata={
                "filename": path.name,
                "extension": path.suffix,
            },
        )