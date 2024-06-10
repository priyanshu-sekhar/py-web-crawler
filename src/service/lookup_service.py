from src.cache.local_cache import LocalCache
from src.cache.redis_cache import RedisCache
from src.service.base_service import BaseService


class LookupService(BaseService):
    def __init__(self):
        self.cache = None

    async def __aenter__(self):
        redis_cache = RedisCache()
        is_redis_cache_enabled = await redis_cache.setup()
        if is_redis_cache_enabled:
            self.cache = redis_cache
        else:
            self.cache = LocalCache()
            await self.cache.setup()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cache.terminate()

    async def check_if_seen_and_update(self, url) -> bool:
        return await self.cache.check_if_seen_and_update(url)



