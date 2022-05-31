from typing import Optional

from aioredis import Redis

redis: Optional[Redis] = None


# Подключаем Redis
async def get_redis() -> Redis:
    return redis
