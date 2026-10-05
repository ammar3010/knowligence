from pathlib import Path

from app.ingestion.loader import BaseDocumentLoader
from app.ingestion.parsers.csv import CSVDocumentLoader
from app.ingestion.parsers.markdown import MarkdownDocumentLoader
from app.ingestion.parsers.pdf import PDFDocumentLoader
from app.ingestion.parsers.text import TextDocumentLoader
from app.ingestion.parsers.web import WebDocumentLoader


class DocumentLoaderFactory:

    @staticmethod
    def get_loader(source: str) -> BaseDocumentLoader:

        if source.startswith(("http://", "https://")):
            return WebDocumentLoader()

        extension = Path(source).suffix.lower()

        loaders = {
            ".pdf": PDFDocumentLoader,
            ".md": MarkdownDocumentLoader,
            ".markdown": MarkdownDocumentLoader,
            ".txt": TextDocumentLoader,
            ".csv": CSVDocumentLoader,
        }

        loader_class = loaders.get(extension)

        if loader_class is None:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        return loader_class()