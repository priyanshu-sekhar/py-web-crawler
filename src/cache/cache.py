from abc import ABC


class Cache(ABC):
    async def check_if_seen_and_update(self, url) -> bool:
        pass
