# app/ingestion/loaders.py

import csv
from pathlib import Path

import fitz
from bs4 import BeautifulSoup

from app.models.documents import Document, DocumentType


class BaseDocumentLoader:
    def load(self, source: str) -> Document:
        raise NotImplementedError


class TextDocumentLoader(BaseDocumentLoader):
    def load(self, source: str) -> Document:
        path = Path(source)

        return Document(
            id="",
            title=path.stem,
            source=str(path),
            source_type=DocumentType.TEXT,
            content=path.read_text(encoding="utf-8"),
        )


class MarkdownDocumentLoader(BaseDocumentLoader):
    def load(self, source: str) -> Document:
        path = Path(source)

        return Document(
            id="",
            title=path.stem,
            source=str(path),
            source_type=DocumentType.MARKDOWN,
            content=path.read_text(encoding="utf-8"),
        )


class PDFDocumentLoader(BaseDocumentLoader):
    def load(self, source: str) -> Document:
        path = Path(source)

        pages = []

        with fitz.open(source) as pdf:
            for page in pdf:
                text = page.get_text().strip()
                if text:
                    pages.append(text)

        return Document(
            id="",
            title=path.stem,
            source=str(path),
            source_type=DocumentType.PDF,
            content="\n\n".join(pages),
            metadata={
                "page_count": len(pages),
            },
        )


class CSVDocumentLoader(BaseDocumentLoader):
    def load(self, source: str) -> Document:
        path = Path(source)

        rows = []

        with path.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                rows.append(
                    " | ".join(
                        f"{key}: {value}"
                        for key, value in row.items()
                    )
                )

        return Document(
            id="",
            title=path.stem,
            source=str(path),
            source_type=DocumentType.CSV,
            content="\n\n".join(rows),
        )


def get_loader(document_type: DocumentType) -> BaseDocumentLoader:
    loaders = {
        DocumentType.TEXT: TextDocumentLoader(),
        DocumentType.MARKDOWN: MarkdownDocumentLoader(),
        DocumentType.PDF: PDFDocumentLoader(),
        DocumentType.CSV: CSVDocumentLoader(),
    }

    try:
        return loaders[document_type]
    except KeyError:
        raise ValueError(
            f"Unsupported document type: {document_type}"
        )