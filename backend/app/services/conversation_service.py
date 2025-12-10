from datetime import datetime
from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.conversation import Conversation
from ..models.message import Message
from ..services.schemas import ConversationEvent, ConversationMessage
from ..core.logger import logger


async def ingest_message_event(session: AsyncSession, event: ConversationEvent) -> Conversation:
    existing = await session.execute(select(Conversation).filter_by(external_id=event.external_id))
    conversation = existing.scalars().first()

    if not conversation:
        conversation = Conversation(
            source=event.source,
            external_id=event.external_id,
            metadata=event.metadata,
        )
        session.add(conversation)
        await session.flush()

    await persist_messages(session, conversation.id, event.messages)
    await session.commit()

    logger.debug("Conversation %s stored", conversation.external_id)
    return conversation


async def persist_messages(session: AsyncSession, conv_id: int, messages: Iterable[ConversationMessage]) -> None:
    to_insert = [
        Message(
            conversation_id=conv_id,
            sender=msg.sender,
            channel=msg.channel,
            content=msg.content,
            ai_outcome={},
            created_at=_parse_timestamp(msg.timestamp),
        )
        for msg in messages
    ]
    session.add_all(to_insert)


def _parse_timestamp(timestamp: str) -> datetime:
    try:
        return datetime.fromisoformat(timestamp)
    except ValueError:
        logger.warning("Invalid timestamp %s, defaulting to now", timestamp)
        return datetime.utcnow()
