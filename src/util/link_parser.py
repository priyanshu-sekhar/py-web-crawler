from urllib.parse import urljoin, urlparse, urldefrag

from bs4 import BeautifulSoup


class LinkParser:
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

    @staticmethod
    async def get_html_links(base_url: str, response):
        if not LinkParser.is_html_response(response):
            return []
        html_content = await response.text()

        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        link_hrefs = [link.get("href") for link in links]
        link_urls = [urljoin(base_url, href) for href in link_hrefs]

        return link_urls

    @staticmethod
    async def get_subdomain_links(base_url: str, response) -> list[str]:
        url_domain = LinkParser.domain_from_url(base_url)
        links = await LinkParser.get_html_links(base_url, response)
        unique_defragmented_links = LinkParser.get_unique_defragmented_links(links)
        return [link for link in unique_defragmented_links if LinkParser.domain_from_url(link) == url_domain]
