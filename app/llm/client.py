import os
from typing import List, Dict

class LiteLLMClient:
    """
    Safe LiteLLM client.
    - NEVER crashes at import time
    - Becomes a no-op if API key is missing
    """

    def __init__(self):
        self.api_key = os.getenv("LITELLM_API_KEY")
        self.enabled = bool(self.api_key)

    def chat(self, messages: List[Dict[str, str]]) -> str:
        if not self.enabled:
            raise RuntimeError("LLM not available")

        # Import here to avoid hard dependency at startup
        from openai import OpenAI

        client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("OPENAI_BASE_URL"),
        )

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=messages,
        )

        return response.choices[0].message.content
