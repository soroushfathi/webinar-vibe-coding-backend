from fastapi import APIRouter, Depends, HTTPException, Header, Request

from ..core.logger import logger
from ..core.config import get_settings
from ..services.odoo_client import OdooClient
from ..services.schemas import ConversationEvent

router = APIRouter(prefix="/odoo", tags=["odoo"])
settings = get_settings()


async def _validate_token(x_api_key: str | None = Header(None)) -> None:
    if x_api_key != settings.odoo_api_key:
        logger.warning("Rejected webhook without valid token")
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post(
    "/webhook",
    dependencies=[Depends(_validate_token)],
    summary="Receives Odoo CRM events",
)
async def odoo_webhook(event: ConversationEvent, request: Request) -> dict[str, str]:
    logger.info("Received Odoo webhook for %s", event.external_id)
    odoo = OdooClient()
    await odoo.sync_lead(event)
    return {"status": "processed"}
