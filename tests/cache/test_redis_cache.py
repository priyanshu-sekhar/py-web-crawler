import unittest
from unittest.mock import patch, Mock, AsyncMock

import asynctest

from src.cache.redis_cache import RedisCache


class RedisCacheTests(asynctest.TestCase):
    @patch('aioredis.from_url')
    async def test_redis_cache_setup_connects_to_redis(self, mock_from_url):
        cache = RedisCache()
        await cache.setup()
        mock_from_url.assert_called_once_with("redis://localhost")

    @patch('aioredis.from_url')
    async def test_redis_cache_setup_handles_connection_error(self, mock_from_url):
        mock_from_url.side_effect = Exception('Connection error')
        cache = RedisCache()
        result = await cache.setup()
        self.assertFalse(result)

    @patch('src.cache.redis_cache.RedisCache', new_callable=AsyncMock)
    async def test_redis_cache_terminate_closes_connection(self, mock_redis):
        cache = RedisCache()
        cache.redis = mock_redis
        await cache.terminate()
        mock_redis.close.assert_called_once()

    @patch('src.cache.redis_cache.RedisCache', new_callable=AsyncMock)
    async def test_redis_cache_check_if_seen_and_update_handles_seen_url(self, mock_redis):
        mock_redis.sismember.return_value = True
        cache = RedisCache()
        cache.redis = mock_redis
        result = await cache.check_if_seen_and_update('http://test.com')
        self.assertTrue(result)

    @patch('src.cache.redis_cache.RedisCache', new_callable=AsyncMock)
    async def test_redis_cache_check_if_seen_and_update_handles_unseen_url(self, mock_redis):
        mock_redis.sismember.return_value = False
        cache = RedisCache()
        cache.redis = mock_redis
        result = await cache.check_if_seen_and_update('http://test.com')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
