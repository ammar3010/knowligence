from pathlib import Path

import pymupdf as fitz

from app.ingestion.loader import BaseDocumentLoader
from app.models.documents import Document, DocumentType
from app.utilities.ids import generate_id


class PDFDocumentLoader(BaseDocumentLoader):

    def load(self, source: str) -> Document:
        path = Path(source)

        document = fitz.open(path)

        pages = []

        for page_number, page in enumerate(document):
            text = page.get_text()

            if text.strip():
                pages.append(
                    f"\n--- Page {page_number + 1} ---\n{text}"
                )

        document.close()

        content = "\n".join(pages)

        return Document(
            id=generate_id("doc"),
            title=path.stem,
            source=str(path.absolute()),
            source_type=DocumentType.PDF,
            content=content,
            metadata={
                "filename": path.name,
                "extension": path.suffix,
                "page_count": len(pages),
            },
        )