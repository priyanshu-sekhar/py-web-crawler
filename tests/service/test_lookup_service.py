import unittest
from unittest.mock import patch, Mock
from src.service.lookup_service import LookupService


class TestLookupService(unittest.TestCase):
    @patch('src.service.lookup_service.RedisCache')
    @patch('src.service.lookup_service.LocalCache')
    async def test_setup_uses_redis_cache_when_enabled(self, mock_local_cache, mock_redis_cache):
        mock_redis_cache.return_value.setup.return_value = True

        service = LookupService()
        await service.setup()

        self.assertIsInstance(service.cache, mock_redis_cache)

    @patch('src.service.lookup_service.RedisCache')
    @patch('src.service.lookup_service.LocalCache')
    async def test_setup_uses_local_cache_when_redis_cache_disabled(self, mock_local_cache, mock_redis_cache):
        mock_redis_cache.return_value.setup.return_value = False

        service = LookupService()
        await service.setup()

        self.assertIsInstance(service.cache, mock_local_cache)

    @patch('src.service.lookup_service.RedisCache')
    async def test_check_if_seen_and_update_calls_cache_method(self, mock_redis_cache):
        mock_redis_cache.return_value.setup.return_value = True
        mock_redis_cache.return_value.check_if_seen_and_update.return_value = True

        service = LookupService()
        await service.setup()
        result = await service.check_if_seen_and_update('http://example.com')

        self.assertTrue(result)
        mock_redis_cache.return_value.check_if_seen_and_update.assert_called_once_with('http://example.com')


if __name__ == '__main__':
    unittest.main()
