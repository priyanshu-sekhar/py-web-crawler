from urllib.parse import urljoin

import robotexclusionrulesparser

from src.service.base_service import BaseService


class RobotsService(BaseService):
    def __init__(self):
        self.robots_parser = robotexclusionrulesparser.RobotFileParserLookalike()

    def can_crawl(self, url):
        """
        Returns True if the URL can be crawled
        """
        try:
            self.robots_parser.set_url(urljoin(url, "/robots.txt"))
            self.robots_parser.read()
            return self.robots_parser.can_fetch("*", url)
        except Exception as e:
            print(f"Error parsing robots.txt for {url}: {e}")
            return False
