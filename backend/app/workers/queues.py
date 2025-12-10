import aio_pika

from ..core.config import get_settings

settings = get_settings()

AI_TASK_QUEUE = "ai_pipeline"


async def declare_queue(channel: aio_pika.RobustChannel) -> aio_pika.Queue:
    return await channel.declare_queue(AI_TASK_QUEUE, durable=True)
