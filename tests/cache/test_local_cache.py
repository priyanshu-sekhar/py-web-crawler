import unittest

import asynctest

from src.cache.local_cache import LocalCache


class LocalCacheTests(asynctest.TestCase):
    async def test_local_cache_check_if_seen_and_update_handles_seen_url(self):
        cache = LocalCache()
        cache.seen.add('http://test.com')
        result = await cache.check_if_seen_and_update('http://test.com')
        self.assertTrue(result)

    async def test_local_cache_check_if_seen_and_update_handles_unseen_url(self):
        cache = LocalCache()
        result = await cache.check_if_seen_and_update('http://test.com')
        self.assertFalse(result)

    async def test_local_cache_check_if_seen_and_update_adds_unseen_url(self):
        cache = LocalCache()
        await cache.check_if_seen_and_update('http://test.com')
        self.assertIn('http://test.com', cache.seen)


if __name__ == '__main__':
    unittest.main()
