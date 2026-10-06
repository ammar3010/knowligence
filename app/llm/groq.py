import json
import logging

from groq import Groq

from app.core.config import get_settings
from app.models.graph import GraphExtraction

logger = logging.getLogger(__name__)


class GroqClient:

    def __init__(self):
        settings = get_settings()

        self.client = Groq(
            api_key=settings.groq_api_key
        )

        self.model = settings.groq_model
        self.extraction_model = settings.groq_extraction_model

    def verify_connection(self) -> bool:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Say OK.",
                    }
                ],
                max_tokens=20,
            )

            return bool(response.choices)

        except Exception:
            logger.exception("Groq connectivity check failed")
            return False

    def extract_query_entities(self, prompt: str) -> list[str]:
        logger.debug("Requesting query entity extraction: model=%s", self.extraction_model)
        try:
            response = self.client.chat.completions.create(
            model=self.extraction_model,
            messages=[
                {
                    "role": "system",
                    "content": "Extract named entities and return only valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=256,
            )
        except Exception:
            logger.exception("Groq query entity extraction failed: model=%s", self.extraction_model)
            raise

        content = response.choices[0].message.content

        if not content:
            logger.warning("Groq returned an empty query entity response")
            raise ValueError("Groq returned an empty response.")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            logger.warning("Groq returned invalid query entity JSON: response_chars=%d", len(content))
            raise ValueError("Groq returned invalid JSON.") from exc

        entities = data.get("entities", [])
        logger.debug("Query entity extraction completed: entity_count=%d", len(entities))
        return entities

    def extract_graph(
    self,
    prompt: str,
) -> GraphExtraction:

        logger.debug("Requesting graph extraction: model=%s", self.extraction_model)
        try:
            response = self.client.chat.completions.create(
            model=self.extraction_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract entities and relationships from text. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=2048,
            )
        except Exception:
            logger.exception("Groq graph extraction request failed: model=%s", self.extraction_model)
            raise

        choice = response.choices[0]

        content = choice.message.content

        logger.debug("Groq graph extraction response received: finish_reason=%s", choice.finish_reason)

        if not content:
            logger.warning("Groq returned an empty graph extraction response: finish_reason=%s", choice.finish_reason)
            raise ValueError(
                f"Groq returned an empty response. "
                f"Finish reason: {choice.finish_reason}"
            )

        try:
            data = json.loads(content)

        except json.JSONDecodeError as exc:
            logger.warning("Groq returned invalid graph extraction JSON: response_chars=%d", len(content))

            raise ValueError(
                "Groq returned invalid JSON."
            ) from exc

        extraction = GraphExtraction.model_validate(data)
        logger.debug(
            "Graph extraction completed: entities=%d relationships=%d",
            len(extraction.entities),
            len(extraction.relationships),
        )
        return extraction

    def generate_answer(self, prompt: str) -> str:
        logger.debug("Requesting answer generation: model=%s", self.model)
        try:
            response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer questions using only the provided evidence. "
                        "Do not invent information."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=2048,
            )
        except Exception:
            logger.exception("Groq answer generation failed: model=%s", self.model)
            raise

        content = response.choices[0].message.content

        if not content:
            logger.warning("Groq returned an empty answer")
            raise ValueError("Groq returned an empty answer.")

        answer = content.strip()
        logger.debug("Answer generation completed: answer_chars=%d", len(answer))
        return answer

    def stream_answer(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer questions using only the provided evidence. "
                        "Do not invent information."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=2048,
            stream=True,
        )

        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                yield delta.content


groq_client = GroqClient()