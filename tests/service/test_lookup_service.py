import asynctest
from unittest.mock import patch, AsyncMock

from src.service.lookup_service import LookupService
from src.cache.local_cache import LocalCache
from src.cache.redis_cache import RedisCache


class LookupServiceTests(asynctest.TestCase):

    @patch.object(RedisCache, '__aenter__', new_callable=AsyncMock)
    async def test_when_redis_cache_is_enabled_uses_redis_cache(self, mock_redis_cache_aenter):
        mock_redis_cache_aenter.return_value = True

        service = LookupService()
        await service.__aenter__()

        self.assertIsInstance(service.cache, RedisCache)

    @patch.object(RedisCache, '__aenter__', new_callable=AsyncMock)
    async def test_when_redis_cache_is_disabled_uses_local_cache(self, mock_redis_cache_aenter):
        mock_redis_cache_aenter.return_value = False

        service = LookupService()
        await service.__aenter__()

        self.assertIsInstance(service.cache, LocalCache)

    @patch.object(LocalCache, 'check_if_seen_and_update', new_callable=AsyncMock)
    @patch.object(RedisCache, '__aenter__', new_callable=AsyncMock)
    async def test_check_if_seen_and_update_calls_cache_method(self, mock_redis_cache_aenter,
                                                          mock_local_cache_check_if_seen_and_update):
        mock_redis_cache_aenter.return_value = False
        mock_local_cache_check_if_seen_and_update.return_value = True

        service = LookupService()
        await service.__aenter__()

        result = await service.check_if_seen_and_update('https://test.com')

        mock_local_cache_check_if_seen_and_update.assert_called_once_with('https://test.com')
        self.assertTrue(result)
