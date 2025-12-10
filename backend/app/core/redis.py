import aioredis

from .config import get_settings


settings = get_settings()
redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)
