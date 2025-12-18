import os
import time
from openai import OpenAI, APIError

LITELLM_BASE_URL = "http://3.110.18.218"
LITELLM_MODEL_FAST = "gemini-2.5-flash"

class LiteLLMClient:
    def __init__(self):
        api_key = os.getenv("LITELLM_API_KEY")
        if not api_key:
            raise RuntimeError("LITELLM_API_KEY not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url=LITELLM_BASE_URL
        )

    def chat(self, messages, model=LITELLM_MODEL_FAST, max_retries=5):
        base_delay = 1

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                return response.choices[0].message.content

            except APIError as e:
                if e.status_code == 429:
                    wait_time = base_delay * (2 ** attempt)
                    time.sleep(wait_time)
                else:
                    raise e

        raise RuntimeError("LiteLLM failed after retries")
