import asyncio
import time


class RateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.semaphore = asyncio.Semaphore(rate_limit)
        self.last_request = time.monotonic()

    async def wait(self):
        async with self.semaphore:
            current_time = time.monotonic()
            elapsed_time = current_time - self.last_request
            if elapsed_time < 1 / self.rate_limit:
                await asyncio.sleep(1 / self.rate_limit - elapsed_time)
            self.last_request = time.monotonic()
