from typing import Any

import httpx

from ..core.config import get_settings
from ..core.logger import logger

settings = get_settings()


class MCPClient:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(base_url=settings.mcp_api_url, headers={"Authorization": f"Bearer {settings.mcp_api_key}"}, timeout=10)

    async def report_error(self, message: str, context: dict[str, Any] | None = None) -> None:
        payload = {"type": "error", "message": message, "context": context or {}}
        await self.client.post("/logs", json=payload)

    async def request_autofix(self, diff: str, reason: str) -> dict[str, Any]:
        payload = {"type": "autofix", "reason": reason, "diff": diff}
        response = await self.client.post("/autofix", json=payload)
        response.raise_for_status()
        return response.json()

    async def log_inspection(self, evaluation: str, metadata: dict[str, Any]) -> None:
        payload = {"type": "inspection", "evaluation": evaluation, "metadata": metadata}
        await self.client.post("/inspections", json=payload)
