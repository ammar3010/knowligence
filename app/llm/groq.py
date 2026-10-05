import json

from groq import Groq

from app.core.config import get_settings
from app.models.graph import GraphExtraction


class GroqClient:

    def __init__(self):
        settings = get_settings()

        self.client = Groq(
            api_key=settings.groq_api_key
        )

        self.model = settings.groq_model

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

        except Exception as exc:
            print(f"Groq connection failed: {exc}")
            return False

    def extract_graph(
        self,
        prompt: str,
    ) -> GraphExtraction:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured knowledge "
                        "graphs from text."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            response_format={
                "type": "json_object"
            },
        )

        content = response.choices[0].message.content

        data = json.loads(content)

        return GraphExtraction.model_validate(data)


groq_client = GroqClient()