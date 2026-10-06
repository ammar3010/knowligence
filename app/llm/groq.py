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

        except Exception as exc:
            print(f"Groq connection failed: {exc}")
            return False

    def extract_graph(
    self,
    prompt: str,
) -> GraphExtraction:

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

        choice = response.choices[0]

        content = choice.message.content

        print("Groq finish reason:", choice.finish_reason)
        print("Groq response:", content)

        if not content:
            raise ValueError(
                f"Groq returned an empty response. "
                f"Finish reason: {choice.finish_reason}"
            )

        try:
            data = json.loads(content)

        except json.JSONDecodeError as exc:
            print("Invalid Groq JSON:")
            print(content)

            raise ValueError(
                "Groq returned invalid JSON."
            ) from exc

        return GraphExtraction.model_validate(data)


groq_client = GroqClient()