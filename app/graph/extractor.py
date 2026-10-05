from app.llm.groq import groq_client
from app.llm.prompts import GRAPH_EXTRACTION_PROMPT
from app.models.documents import DocumentChunk
from app.models.graph import GraphExtraction


class GraphExtractor:

    def extract(
        self,
        chunk: DocumentChunk,
    ) -> GraphExtraction:

        prompt = GRAPH_EXTRACTION_PROMPT.format(
            text=chunk.content
        )

        return groq_client.extract_graph(prompt)