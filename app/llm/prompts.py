GRAPH_EXTRACTION_PROMPT = """
You are a knowledge graph extraction system.

Extract factual entities and relationships from the provided text.

Entities should represent important real-world concepts such as:
- companies
- organizations
- people
- products
- technologies
- locations
- events

Relationships should describe factual connections between entities.

Rules:
1. Only extract information explicitly supported by the text.
2. Do not invent facts.
3. Use concise entity names.
4. Use uppercase snake_case for relationship names.
5. Avoid duplicate entities.
6. Relationships must reference entities that appear in the entity list.
7. Prefer specific relationships such as:
   INVESTED_IN
   ACQUIRED
   FOUNDED
   WORKED_WITH
   PARTNERED_WITH
   DEVELOPED
   LOCATED_IN
   EMPLOYED
   USES

Return valid JSON matching this structure:

{
    "entities": [
        {
            "name": "string",
            "type": "string",
            "description": "string"
        }
    ],
    "relationships": [
        {
            "source": "string",
            "source_type": "string",
            "relation": "RELATION_TYPE",
            "target": "string",
            "target_type": "string",
            "description": "string"
        }
    ]
}

Text:
{text}
"""