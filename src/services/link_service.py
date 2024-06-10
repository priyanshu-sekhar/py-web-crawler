from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup

from src.services.base_service import BaseService
from src.services.session_service import SessionService


class LinkService(BaseService):
    def __init__(self):
        self.session_service = SessionService()

    async def setup(self):
        return await self.session_service.setup()

    async def terminate(self):
        return await self.session_service.terminate()

    @staticmethod
    def domain_from_url(url):
        return f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    @staticmethod
    def get_unique_defragmented_links(links: list[str]) -> list[str]:
        return list(set([urldefrag(link)[0] for link in links]))

    @staticmethod
    def is_html_response(response) -> bool:
        content_type = response.headers.get("content-type")
        return content_type and "text/html" in content_type

    async def get_html_links(self, base_url: str):
        response = await self.session_service.get(base_url)
        if not self.is_html_response(response):
            return []
        html_content = await response.text()

        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        link_hrefs = [link.get("href") for link in links]
        link_urls = [urljoin(base_url, href) for href in link_hrefs]

        return link_urls

    async def get_subdomain_links(self, base_url: str) -> list[str]:
        url_domain = self.domain_from_url(base_url)
        links = await self.get_html_links(base_url)
        unique_defragmented_links = self.get_unique_defragmented_links(links)
        return [link for link in unique_defragmented_links if self.domain_from_url(link) == url_domain]
