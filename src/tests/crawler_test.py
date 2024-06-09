import unittest
from unittest.mock import patch, MagicMock
from src.crawler import Crawler


class CrawlerTests(unittest.TestCase):
    @patch("src.crawler.aiohttp.ClientSession.get")
    @patch("src.crawler.aiofiles.open")
    async def tet_crawl_all_links(self, mock_file, mock_get):
        mock_get.return_value.__aenter__.return_value.text.return_value = \
            '<html><body><a href="https://example.com"></a></body></html>'
        mock_file.return_value.__aenter__.return_value.write.return_value = MagicMock()
        crawler = Crawler("http://example.com")
        await crawler.crawl()
        mock_file.return_value.__aenter__.return_value.write.assert_called_once_with("https://example.com\n")


if __name__ == '__main__':
    unittest.main()
