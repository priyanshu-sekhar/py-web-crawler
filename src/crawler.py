import asyncio

from src.services.file_service import FileService
from src.services.link_service import LinkService
from src.services.lookup_service import LookupService
from src.services.rate_limit_service import RateLimitService
from src.services.robots_service import RobotsService
from src.services.session_service import SessionService


class Crawler:
    def __init__(self, start_url, file_name, rate_limit=1):
        self.start_url = start_url
        self.file_name = file_name
        self.file_service = FileService(file_name)
        self.session_service = SessionService()
        self.link_service = LinkService()
        self.rate_limit_service = RateLimitService(rate_limit)
        self.lookup_service = LookupService()
        self.robots_service = RobotsService()

    async def crawl(self):
        try:
            await self.__setup()
            await self._crawl([self.start_url])
        finally:
            await self.__teardown()

    async def _crawl(self, urls):
        for url in urls:
            try:
                if await self.lookup_service.check_if_seen_and_update(url):
                    continue
                if not self.robots_service.can_crawl(url):
                    continue
                await self.file_service.write_to_file(url)
                self.rate_limit_service.wait()
                link_urls = await self.link_service.get_subdomain_links(url)
                await self._crawl(link_urls)
            except Exception as e:
                print(f"Error crawling {url}: {e}")

    async def __setup(self):
        await self.lookup_service.setup()
        await self.file_service.setup()
        await self.link_service.setup()
        await self.rate_limit_service.setup()
        await self.robots_service.setup()
        await self.session_service.setup()
        await self.lookup_service.restore_from_cache(self.file_name)

    async def __teardown(self):
        await self.lookup_service.terminate()
        await self.file_service.terminate()
        await self.link_service.terminate()
        await self.rate_limit_service.terminate()
        await self.robots_service.terminate()
        await self.session_service.terminate()


if __name__ == '__main__':
    site_to_crawl = "https://monzo.com"
    links_file = "monzo-links.txt"
    crawl_rate_limit = 1
    crawler = Crawler(start_url=site_to_crawl, file_name=links_file, rate_limit=crawl_rate_limit)
    asyncio.run(crawler.crawl())
