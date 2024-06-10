from src.services.base_service import BaseService
from src.services.redis_service import RedisService


class LookupService(BaseService):
    def __init__(self):
        self.cache_service = RedisService()
        self.seen = set()
        self.cache_enabled = False

    async def setup(self):
        self.cache_enabled = await self.cache_service.setup()

    async def terminate(self):
        await self.cache_service.terminate()

    async def restore_from_cache(self, file_name):
        await self.cache_service.dump_to_file(file_name)

    async def check_if_seen_and_update(self, url) -> bool:
        if self.cache_enabled:
            return await self.cache_service.check_if_seen_and_update(url)
        else:
            if url in self.seen:
                return True
            self.seen.add(url)
            return False



