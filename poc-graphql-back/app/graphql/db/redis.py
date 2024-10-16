from typing import AsyncGenerator

import redis.asyncio as redis

from app.settings import settings


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    async with redis.from_url(settings.REDIS_URL) as redis_client:
        try:
            yield redis_client
        finally:
            await redis_client.close()
