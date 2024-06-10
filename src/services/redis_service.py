import aioredis

from src.services.base_service import BaseService


class RedisService(BaseService):
    def __init__(self):
        self.redis = None

    async def setup(self) -> bool:
        try:
            self.redis = await aioredis.from_url("redis://localhost")
            return True
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            return False

    async def terminate(self):
        if self.redis:
            await self.redis.close()

    async def check_if_seen_and_update(self, url) -> bool:
        seen = False
        if self.redis:
            seen = await self.redis.sismember("seen", url)
            if not seen:
                await self.redis.sadd("seen", url)
        return seen

    async def dump_to_file(self, file_name):
        if self.redis:
            with open(file_name, "w") as f:
                for url in await self.redis.smembers("seen"):
                    # url is of form b'https://example.com'
                    url = url.decode("utf-8")
                    f.write(f"{url}\n")