# openai_config.py
import os
import openai
from typing import List, Optional

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = openai.OpenAI()

def call_openai_chat(
    messages: List[dict],
    model: str = "gpt-4",
    temperature: float = 0.3,
    stream: bool = False,
    functions: Optional[List[dict]] = None
):
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if functions:
        kwargs["functions"] = functions
        kwargs["function_call"] = "auto"
    if stream:
        kwargs["stream"] = True

    return client.chat.completions.create(**kwargs)
