import re

import tiktoken

from app.core.config import get_settings
from app.models.documents import Document, DocumentChunk
from app.utilities.ids import generate_id


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        settings = get_settings()

        self.chunk_size = (
            chunk_size
            if chunk_size is not None
            else settings.chunk_size
        )

        self.chunk_overlap = (
            chunk_overlap
            if chunk_overlap is not None
            else settings.chunk_overlap
        )

        self.encoder = tiktoken.get_encoding("cl100k_base")

    def _token_count(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def _split_paragraphs(self, text: str) -> list[str]:
        paragraphs = re.split(r"\n\s*\n", text)

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]

    def _split_large_paragraph(
        self,
        paragraph: str,
    ) -> list[str]:

        tokens = self.encoder.encode(paragraph)

        chunks = []

        start = 0

        while start < len(tokens):
            end = min(
                start + self.chunk_size,
                len(tokens),
            )

            chunk_tokens = tokens[start:end]

            chunks.append(
                self.encoder.decode(chunk_tokens)
            )

            if end >= len(tokens):
                break

            start = end - self.chunk_overlap

        return chunks

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        paragraphs = self._split_paragraphs(
            document.content
        )

        chunks: list[DocumentChunk] = []

        current_parts: list[str] = []
        current_tokens = 0

        for paragraph in paragraphs:

            paragraph_tokens = self._token_count(
                paragraph
            )

            # A single paragraph is larger than our
            # maximum chunk size.
            if paragraph_tokens > self.chunk_size:

                if current_parts:
                    chunks.append(
                        self._create_chunk(
                            document=document,
                            parts=current_parts,
                            index=len(chunks),
                        )
                    )

                    current_parts = []
                    current_tokens = 0

                large_chunks = self._split_large_paragraph(
                    paragraph
                )

                for part in large_chunks:
                    chunks.append(
                        self._create_chunk(
                            document=document,
                            parts=[part],
                            index=len(chunks),
                        )
                    )

                continue

            # Adding this paragraph would exceed
            # the chunk size.
            if (
                current_tokens + paragraph_tokens
                > self.chunk_size
                and current_parts
            ):
                chunks.append(
                    self._create_chunk(
                        document=document,
                        parts=current_parts,
                        index=len(chunks),
                    )
                )

                # Preserve overlap from the end of
                # the previous chunk.
                overlap_parts = []

                overlap_tokens = 0

                for part in reversed(current_parts):
                    part_tokens = self._token_count(part)

                    if (
                        overlap_tokens + part_tokens
                        > self.chunk_overlap
                    ):
                        break

                    overlap_parts.insert(0, part)
                    overlap_tokens += part_tokens

                current_parts = overlap_parts
                current_tokens = overlap_tokens

            current_parts.append(paragraph)
            current_tokens += paragraph_tokens

        if current_parts:
            chunks.append(
                self._create_chunk(
                    document=document,
                    parts=current_parts,
                    index=len(chunks),
                )
            )

        return chunks

    def _create_chunk(
        self,
        document: Document,
        parts: list[str],
        index: int,
    ) -> DocumentChunk:

        content = "\n\n".join(parts).strip()

        return DocumentChunk(
            id=generate_id("chunk"),
            document_id=document.id,
            content=content,
            chunk_index=index,
            token_count=self._token_count(content),
            metadata={
                **document.metadata,
                "source": document.source,
                "title": document.title,
                "source_type": document.source_type.value,
            },
        )