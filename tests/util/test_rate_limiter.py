import unittest
from unittest.mock import patch, Mock, AsyncMock

import asynctest

from src.util.rate_limiter import RateLimiter


class TestRateLimiter(asynctest.IsolatedAsyncioTestCase):
    @patch('src.util.rate_limiter.time.monotonic')
    @patch('src.util.rate_limiter.asyncio.sleep', new_callable=AsyncMock)
    async def test_rate_limiter_waits_when_rate_limit_exceeded(self, mock_sleep, mock_time):
        mock_time.side_effect = [0, 0.5, 0.5]
        rate_limiter = RateLimiter(1)

        await rate_limiter.wait()

        mock_sleep.assert_called_once_with(0.5)

    @patch('src.util.rate_limiter.time.monotonic')
    @patch('src.util.rate_limiter.asyncio.sleep', new_callable=AsyncMock)
    async def test_rate_limiter_does_not_wait_when_rate_limit_not_exceeded(self, mock_sleep, mock_time):
        mock_time.side_effect = [0, 2.0, 2.0]
        rate_limiter = RateLimiter(1)

        await rate_limiter.wait()

        mock_sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()
