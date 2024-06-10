import time

from src.services.base_service import BaseService


class RateLimitService(BaseService):
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.last_request = time.time()

    def wait(self):
        time_since_last_request = time.time() - self.last_request
        sleep_duration = max(0.0, self.rate_limit - time_since_last_request)
        time.sleep(sleep_duration)
        self.last_request = time.time()
