import json
from datetime import datetime
from typing import Literal

import aio_pika

from ..core.logger import logger
from ..core.redis import redis_client
from ..core.mq import get_rabbit_connection
from .schemas import ConversationEvent

AI_TASK_QUEUE = "ai_pipeline"
METRICS_PREFIX = "ai_pipeline:stats"


async def enqueue_ai_task(event: ConversationEvent) -> None:
    payload = {
        "source": event.source,
        "external_id": event.external_id,
        "metadata": event.metadata,
        "messages": [msg.model_dump() for msg in event.messages],
        "ingested_at": datetime.utcnow().isoformat(),
    }

    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(AI_TASK_QUEUE, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode("utf-8"),
                content_type="application/json",
            ),
            routing_key=queue.name,
        )
    await _record_metric("ingested")
    logger.info("Queued AI task for conversation %s", event.external_id)


async def _record_metric(metric: Literal["ingested", "processed"]) -> None:
    now = datetime.utcnow().isoformat()
    await redis_client.zadd(
        f"{METRICS_PREFIX}:{metric}", {now: datetime.utcnow().timestamp()}
    )
