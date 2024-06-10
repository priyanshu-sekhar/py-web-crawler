import asyncio

from src.io.file_io import FileIO
from src.service.lookup_service import LookupService
from src.service.robots_service import RobotsService
from src.service.session_service import SessionService
from src.util.link_parser import LinkParser
from src.util.rate_limiter import RateLimiter


class Crawler:
    def __init__(self, start_url, file_name, rate_limit=10):
        self.start_url = start_url
        self.file_name = file_name
        self.file_service = FileIO(file_name)
        self.session_service = SessionService()
        self.link_parser = LinkParser()
        self.rate_limiter = RateLimiter(rate_limit)
        self.lookup_service = LookupService()
        self.robots_service = RobotsService()

    async def crawl(self):
        try:
            await self.__setup()
            await self._crawl([self.start_url])
        finally:
            await self.__teardown()

    async def _crawl(self, urls):
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.__process_url(url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def __process_url(self, url):
        try:
            if await self.lookup_service.check_if_seen_and_update(url):
                return
            if not self.robots_service.can_crawl(url):
                return
            await self.file_service.write_to_file(url)
            response = await self.session_service.get(url)
            link_urls = await self.link_parser.get_subdomain_links(url, response)
            await self._crawl(link_urls)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    async def __setup(self):
        await self.lookup_service.setup()
        await self.robots_service.setup()
        await self.session_service.setup()

    async def __teardown(self):
        await self.lookup_service.terminate()
        await self.robots_service.terminate()
        await self.session_service.terminate()


if __name__ == '__main__':
    site_to_crawl = "https://monzo.com"
    links_file = "monzo-links.txt"
    crawl_rate_limit = 1
    crawler = Crawler(start_url=site_to_crawl, file_name=links_file, rate_limit=crawl_rate_limit)
    asyncio.run(crawler.crawl())
