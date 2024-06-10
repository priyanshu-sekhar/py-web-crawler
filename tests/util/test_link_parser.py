import unittest
from unittest.mock import patch, Mock, AsyncMock

import asynctest

from src.util.link_parser import LinkParser


class LinkParserTests(asynctest.TestCase):
    @patch('src.util.link_parser.BeautifulSoup')
    @patch('src.util.link_parser.urljoin')
    async def test_link_parser_gets_html_links(self, mock_urljoin, mock_soup):
        mock_response = Mock()
        mock_response.text = AsyncMock(return_value="<html><body><a href='test_link'></a></body></html>")
        mock_response.headers = {'content-type': 'text/html'}
        mock_soup.return_value.find_all.return_value = [{'href': 'test_link'}]
        mock_urljoin.return_value = 'http://test.com/test_link'

        result = await LinkParser.get_html_links('http://test.com', mock_response)

        self.assertEqual(result, ['http://test.com/test_link'])

    @patch('src.util.link_parser.LinkParser.get_html_links')
    @patch('src.util.link_parser.LinkParser.get_unique_defragmented_links')
    async def test_link_parser_gets_subdomain_links(self, mock_get_unique_defragmented_links, mock_get_html_links):
        mock_response = Mock()
        mock_get_html_links.return_value = ['http://test.com/test_link', 'http://test.com/test_link#fragment']
        mock_get_unique_defragmented_links.return_value = ['http://test.com/test_link']

        result = await LinkParser.get_subdomain_links('http://test.com', mock_response)

        self.assertEqual(result, ['http://test.com/test_link'])


if __name__ == '__main__':
    unittest.main()
