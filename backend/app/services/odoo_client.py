from typing import Any

import httpx

from ..core.config import get_settings
from ..core.logger import logger
from ..services.schemas import ConversationEvent

settings = get_settings()


class OdooClient:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(base_url=settings.odoo_api_url, timeout=10)

    async def sync_lead(self, event: ConversationEvent) -> None:
        payload = {
            "name": event.metadata.get("lead_name", "Unknown lead"),
            "external_id": event.external_id,
            "conversation_channel": event.metadata.get("primary_channel", "chat"),
            "state": "new",
            "notes": [msg.content for msg in event.messages],
        }
        response = await self.client.post(
            "/api/leads", json=payload, headers={"X-API-KEY": settings.odoo_api_key}
        )
        response.raise_for_status()
        logger.info("Synced lead %s to Odoo", event.external_id)
