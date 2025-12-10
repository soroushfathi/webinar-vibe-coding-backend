import asyncio
import json
from datetime import datetime

import aio_pika

from ..core.logger import logger
from ..core.redis import redis_client
from ..services.llm_agent import LLMAgent
from ..services.mcp_client import MCPClient
from ..services.ai_pipeline import METRICS_PREFIX
from .queues import AI_TASK_QUEUE, declare_queue
from ..core.config import get_settings
from ..core.mq import get_rabbit_connection

settings = get_settings()


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process(ignore_processed=True):
        payload = json.loads(message.body)
        logger.info("Processing AI task %s", payload["external_id"])

        llm = LLMAgent()
        mcp = MCPClient()

        try:
            summary = await llm.summarize("\n".join([msg["content"] for msg in payload["messages"]]))
            await mcp.log_inspection("Summary generated", {"conversation": payload["external_id"], "summary_length": len(summary)})
            await _record_metric("processed")
        except Exception as exc:
            await mcp.report_error("LLM failure", {"payload": payload, "error": str(exc)})
            logger.exception("LLM pipeline failed")


async def _record_metric(metric: str) -> None:
    await redis_client.zadd(f"{METRICS_PREFIX}:{metric}", {datetime.utcnow().isoformat(): datetime.utcnow().timestamp()})


async def start_worker() -> None:
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        queue = await declare_queue(channel)
        await queue.consume(process_message, no_ack=False)
        logger.info("AI worker is running")
        await asyncio.Event().wait()
