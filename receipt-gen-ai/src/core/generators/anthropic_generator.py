from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from .base import BaseGenerator
import os
from dotenv import load_dotenv

load_dotenv()

class AnthropicGenerator(BaseGenerator):
    def __init__(self, api_key: str = None, model: str = "claude-3-haiku-20240307"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = Anthropic(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"❌ Error with Anthropic API: {e}")
            return ""
