import asyncio
import time
from urllib.parse import urljoin, urlparse, urldefrag

import aiofiles
import aiohttp
# import aioredis
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, start_url, rate_limit=1):
        self.start_url = start_url
        self.rate_limit = rate_limit
        self.last_request = time.time()
        self.seen = set()
        self.session = None
        self.redis = None

    async def crawl(self):
        # try:
        #     self.redis = await aioredis.from_url("redis://localhost")
        # except Exception as e:
        #     print(f"Error connecting to Redis: {e}")
        try:
            self.session = aiohttp.ClientSession()
            await self._crawl([self.start_url])
        except Exception as e:
            print(f"Error creating aiohttp session: {e}")
        finally:
            if self.session:
                await self.session.close()
            if self.redis:
                await self.redis.close()

    async def _crawl(self, urls):
        """
        Crawls the URLs in the list, getting all subdomain links and crawling them as well, writing the URLs to a file
        """
        for url in urls:
            if await self._check_if_seen_and_update(url):
                continue
            await self._write_to_file(url)
            await asyncio.sleep(max(0.0, self.last_request + self.rate_limit - time.time()))
            self.last_request = time.time()
            link_urls = await self._get_subdomain_links(url)
            await self._crawl(link_urls)

    async def _check_if_seen_and_update(self, url):
        """
        Returns True if the URL has already been seen. Checks the Redis cache if available, otherwise uses a set
        """
        if self.redis:
            seen = await self.redis.sismember("seen", url)
            if not seen:
                await self.redis.sadd("seen", url)
        else:
            seen = url in self.seen
            if not seen:
                self.seen.add(url)
        return seen

    @staticmethod
    def _domain_from_url(url):
        """
        Returns the domain of the URL
        """
        return f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    @staticmethod
    def _get_unique_defragmented_links(links: list[str]) -> list[str]:
        """
        Returns unique links after removing fragment identifiers
        """
        return list(set([urldefrag(link)[0] for link in links]))

    @staticmethod
    def _is_html_response(response) -> bool:
        """
        checks content-type of the response and returns True if it is html
        """
        content_type = response.headers.get("content-type")
        return content_type and "text/html" in content_type

    @staticmethod
    async def _write_to_file(url):
        """
        Writes the URL to a file
        """
        async with aiofiles.open('urls.txt', mode='a') as f:
            await f.write(f'{url}\n')

    async def _get_all_links(self, base_url: str):
        """
        Returns all URLs that are found on the page located at `url`
        """
        # Get the HTML content of the page
        response = await self.session.get(base_url)
        if not self._is_html_response(response):
            return []
        html_content = await response.text()

        # Parse the HTML content tp find all links in the page
        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        link_hrefs = [link.get("href") for link in links]
        link_urls = [urljoin(base_url, href) for href in link_hrefs]

        return link_urls

    async def _get_subdomain_links(self, base_url: str) -> list[str]:
        """
        Returns all URLs that are found in url belonging to same subdomain
        """
        url_domain = self._domain_from_url(base_url)
        links = await self._get_all_links(base_url)
        unique_defragmented_links = self._get_unique_defragmented_links(links)
        return [link for link in unique_defragmented_links if self._domain_from_url(link) == url_domain]

    # async def get_nested_subdomain_links(self, base_url: str):
    #     """
    #     Returns all URLs that should be crawled for a given domain
    #     """
    #     output_file = "output.txt"  # Use this if writing to a file
    #     url_link_map: dict[str, list[str]] = {}
    #     url_queue = [base_url]
    #     seen = set()
    #
    #     while url_queue:
    #         new_url = url_queue.pop(0)
    #
    #         if new_url in seen:
    #             continue
    #         self.output(f"Crawling: {new_url}", output_file)
    #         seen.add(new_url)
    #         self.output("Found links:", output_file)
    #
    #         subdomain_links = await self._get_subdomain_links(new_url)
    #         url_link_map.setdefault(new_url, []).extend(subdomain_links)
    #         for link in subdomain_links:
    #             self.output(f"\t{link}", output_file)
    #             url_queue.append(link)
    #
    #     return url_link_map
    #
    # def output(self, text: str, file_name: str):
    #     """
    #     Outputs the text to the console or a file
    #     """
    #     if file_name:
    #         with open(file_name, "a") as file:
    #             file.write(text + "\n")
    #     else:
    #         print(text)

    # start_domain = self.domain_from_url(start_url)
    # return get_nested_subdomain_links(start_domain)


# crawl("https://monzo.com")
if __name__ == '__main__':
    crawler = Crawler("https://monzo.com")
    asyncio.run(crawler.crawl())
