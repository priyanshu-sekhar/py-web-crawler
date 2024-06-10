import unittest
from unittest.mock import patch, Mock
from src.service.robots_service import RobotsService


class TestRobotsService(unittest.TestCase):
    @patch('src.service.robots_service.robotexclusionrulesparser.RobotFileParserLookalike')
    def test_can_crawl_returns_true_when_url_is_allowed(self, mock_robots_parser):
        # Mock the can_fetch method to return True
        mock_robots_parser.return_value.can_fetch.return_value = True

        service = RobotsService()
        result = service.can_crawl('http://example.com')

        self.assertTrue(result)

    @patch('src.service.robots_service.robotexclusionrulesparser.RobotFileParserLookalike')
    def test_can_crawl_returns_false_when_url_is_disallowed(self, mock_robots_parser):
        # Mock the can_fetch method to return False
        mock_robots_parser.return_value.can_fetch.return_value = False

        service = RobotsService()
        result = service.can_crawl('http://example.com')

        self.assertFalse(result)

    @patch('src.service.robots_service.robotexclusionrulesparser.RobotFileParserLookalike')
    def test_can_crawl_returns_false_when_exception_is_raised(self, mock_robots_parser):
        # Mock the can_fetch method to raise an exception
        mock_robots_parser.return_value.can_fetch.side_effect = Exception('Error')

        service = RobotsService()
        result = service.can_crawl('http://example.com')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
