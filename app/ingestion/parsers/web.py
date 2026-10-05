import httpx
from bs4 import BeautifulSoup

from app.ingestion.loader import BaseDocumentLoader
from app.models.documents import Document, DocumentType
from app.utilities.ids import generate_id


class WebDocumentLoader(BaseDocumentLoader):

    def load(self, source: str) -> Document:
        response = httpx.get(
            source,
            timeout=30,
            follow_redirects=True,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        for element in soup(
            ["script", "style", "noscript"]
        ):
            element.decompose()

        content = soup.get_text(
            separator="\n",
            strip=True,
        )

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else source
        )

        return Document(
            id=generate_id("doc"),
            title=title,
            source=source,
            source_type=DocumentType.WEB,
            content=content,
            metadata={
                "url": source,
            },
        )