import unittest
from unittest.mock import patch, AsyncMock

import asynctest

from src.crawler import Crawler


class CrawlerTests(asynctest.TestCase):

    @patch('src.crawler.SessionService.setup', new_callable=AsyncMock)
    @patch('src.crawler.SessionService.terminate', new_callable=AsyncMock)
    @patch('src.crawler.LookupService.setup', new_callable=AsyncMock)
    @patch('src.crawler.LookupService.terminate', new_callable=AsyncMock)
    @patch('src.crawler.RobotsService.setup', new_callable=AsyncMock)
    @patch('src.crawler.RobotsService.terminate', new_callable=AsyncMock)
    async def test_crawler_crawl_calls_setup_and_teardown(self,
                                                          mock_robots_service_terminate, mock_robots_service_setup,
                                                          mock_lookup_service_terminate, mock_lookup_service_setup,
                                                          mock_session_service_terminate, mock_session_service_setup):
        crawler = Crawler('http://test.com', 'test.txt')
        crawler._crawl = AsyncMock()
        await crawler.crawl()
        mock_lookup_service_setup.assert_called_once()
        mock_robots_service_setup.assert_called_once()
        mock_session_service_setup.assert_called_once()
        mock_lookup_service_terminate.assert_called_once()
        mock_robots_service_terminate.assert_called_once()
        mock_session_service_terminate.assert_called_once()

    @patch('src.crawler.FileIO')
    @patch('src.crawler.LookupService', new_callable=AsyncMock)
    async def test_crawler_process_url_skips_seen_url(self, mock_lookup_service, mock_file_io):
        crawler = Crawler('http://test.com', 'test.txt')
        mock_lookup_service.check_if_seen_and_update.return_value = True
        await crawler._Crawler__process_url('http://test.com')
        mock_file_io.write_to_file.assert_not_called()

    @patch('src.crawler.FileIO')
    @patch('src.crawler.LookupService')
    @patch('src.crawler.RobotsService')
    async def test_crawler_process_url_skips_url_when_robots_disallow(self, mock_robots_service, mock_lookup_service,
                                                                      mock_file_io):
        crawler = Crawler('http://test.com', 'test.txt')
        mock_lookup_service.check_if_seen_and_update.return_value = False
        mock_robots_service.can_crawl.return_value = False
        await crawler._Crawler__process_url('http://test.com')
        mock_file_io.write_to_file.assert_not_called()


if __name__ == '__main__':
    unittest.main()
