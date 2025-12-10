from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import AsyncSessionLocal
from ..core.logger import logger
from ..services.ai_pipeline import enqueue_ai_task
from ..services.conversation_service import ingest_message_event
from ..services.schemas import ConversationEvent

router = APIRouter(prefix="/conversation", tags=["conversation"])


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/ingest", summary="Ingest conversation events")
async def ingest_event(event: ConversationEvent, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    logger.info("Ingesting event for %s", event.source)
    try:
        await ingest_message_event(session=session, event=event)
        await enqueue_ai_task(event)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to ingest conversation event")
        raise HTTPException(status_code=500, detail="Unable to process event")
    return {"status": "queued"}
