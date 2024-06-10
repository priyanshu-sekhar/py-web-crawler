from src.cache.cache import Cache


class LocalCache(Cache):
    def __init__(self):
        self.seen = set()

    async def check_if_seen_and_update(self, url) -> bool:
        if url in self.seen:
            return True
        self.seen.add(url)
        return False
