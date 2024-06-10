import unittest
from unittest.mock import patch, AsyncMock

import asynctest

from src.crawler import Crawler


class CrawlerTests(asynctest.TestCase):

    @patch('src.crawler.Crawler._crawl', new_callable=AsyncMock)
    async def test_crawler_crawl_calls_aenter_and_aexit(self, mock_crawl):
        with patch('src.crawler.LookupService.__aenter__', new_callable=AsyncMock) as mock_lookup_service_aenter, \
             patch('src.crawler.LookupService.__aexit__', new_callable=AsyncMock) as mock_lookup_service_aexit, \
             patch('src.crawler.SessionService.__aenter__', new_callable=AsyncMock) as mock_session_service_aenter, \
             patch('src.crawler.SessionService.__aexit__', new_callable=AsyncMock) as mock_session_service_aexit:

            crawler = Crawler('https://test.com', 'test.txt')
            await crawler.crawl()

            mock_lookup_service_aenter.assert_called_once()
            mock_session_service_aenter.assert_called_once()
            mock_lookup_service_aexit.assert_called_once()
            mock_session_service_aexit.assert_called_once()

    @patch('src.crawler.FileIO')
    @patch('src.crawler.LookupService', new_callable=AsyncMock)
    async def test_crawler_process_url_skips_seen_url(self, mock_lookup_service, mock_file_io):
        crawler = Crawler('https://test.com', 'test.txt')
        mock_lookup_service.check_if_seen_and_update.return_value = True
        await crawler._process_url('https://test.com')
        mock_file_io.write_to_file.assert_not_called()

    @patch('src.crawler.FileIO')
    @patch('src.crawler.LookupService')
    @patch('src.crawler.RobotsService')
    async def test_crawler_process_url_skips_url_when_robots_disallow(self, mock_robots_service, mock_lookup_service,
                                                                      mock_file_io):
        crawler = Crawler('https://test.com', 'test.txt')
        mock_lookup_service.check_if_seen_and_update.return_value = False
        mock_robots_service.can_crawl.return_value = False
        await crawler._process_url('https://test.com')
        mock_file_io.write_to_file.assert_not_called()


if __name__ == '__main__':
    unittest.main()
