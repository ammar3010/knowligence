GRAPH_EXTRACTION_PROMPT = """
Extract the entities and factual relationships from this text.

Return ONLY valid JSON.
Do not return markdown.
Do not explain your answer.

Required JSON:

{
  "entities": [
    {
      "name": "entity name",
      "type": "COMPANY",
      "description": "short description"
    }
  ],
  "relationships": [
    {
      "source": "source entity",
      "source_type": "COMPANY",
      "relation": "RELATION",
      "target": "target entity",
      "target_type": "COMPANY",
      "description": "short description"
    }
  ]
}

Rules:
- Extract only facts explicitly stated in the text.
- Do not invent facts.
- Include important companies, organizations, people, products, technologies, locations and events.
- Relationship names must use uppercase snake_case.
- Every relationship source and target must exist in entities.
- If none exist, use an empty array.

TEXT:

{text}
"""