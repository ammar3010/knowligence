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

ANSWER_PROMPT = """
You are a knowledge intelligence assistant.

Answer the user's question using ONLY the provided evidence and conversation history.

Strict grounding rules:
- Every factual claim about the knowledge base must be directly supported by the evidence.
- Do NOT use outside knowledge.
- Do NOT infer, assume, or expand relationships beyond what the evidence states.
- Do NOT add facts that are merely plausible.
- Preserve the exact meaning of the source evidence.
- Use conversation history only to understand references and conversational context.
- If the user refers to something like "it", "they", "that company", or "the previous one",
  resolve the reference using conversation history.
- For multi-hop questions, explicitly show each relationship in the chain.
- If the evidence is insufficient to answer the question, say so.
- Keep the answer concise and clear.

CONVERSATION HISTORY:
{chat_history}

QUESTION:
{query}

EVIDENCE:
{context}

ANSWER:
"""