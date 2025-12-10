import aio_pika

from .config import get_settings


settings = get_settings()

async def get_rabbit_connection() -> aio_pika.RobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)

async def get_rabbit_channel() -> aio_pika.RobustChannel:
    connection = await get_rabbit_connection()
    return await connection.channel()
