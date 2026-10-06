from app.llm.groq import groq_client


QUERY_ENTITY_PROMPT = """
Identify the important named entities in the user's question.

Return ONLY valid JSON in this exact format:

{
  "entities": ["Entity 1", "Entity 2"]
}

Rules:
- Extract only entities explicitly mentioned in the question.
- Preserve the entity's original name.
- Do not add outside knowledge.
- Do not explain anything.
- If there are no named entities, return an empty list.

QUESTION:
{query}
"""


class QueryEntityExtractor:
    def extract(self, query: str) -> list[str]:
        prompt = QUERY_ENTITY_PROMPT.replace("{query}", query)

        return groq_client.extract_query_entities(prompt)