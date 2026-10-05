from groq import Groq

from app.core.config import get_settings


class GroqClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = Groq(
            api_key=settings.groq_api_key,
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

groq_client = GroqClient()