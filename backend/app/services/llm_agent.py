from typing import Any

import asyncio
from openai import AsyncOpenAI

from ..core.config import get_settings
from ..core.logger import logger

settings = get_settings()


class LLMAgent:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def call_llm(self, prompt: str, model: str = "gpt-4o-mini") -> dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are an AI assistant"}, {"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=500,
        )
        return response.to_dict()

    async def summarize(self, conversation: str) -> str:
        response = await self.call_llm(f"Summarize this conversation:\n{conversation}")
        return response["choices"][0]["message"]["content"]
