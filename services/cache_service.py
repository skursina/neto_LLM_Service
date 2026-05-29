import asyncio
import logging

from cachetools import TTLCache
from config.settings import settings

logger = logging.getLogger(__name__)

cache = TTLCache(maxsize=settings.cache_maxsize, ttl=settings.cache_ttl)
_cache_lock = asyncio.Lock()

async def get_cached(key: str) -> str | None:
    async with _cache_lock:
        value = cache.get(key)
        if value is not None:
            logger.info(f"Cache hit: {key}")
        else:
            logger.info(f"Cache miss: {key}")
        return value

async def set_cache(key: str, value: str) -> None:
    async with _cache_lock:
        cache[key] = value
        logger.info(f"Cache saved: {key}")