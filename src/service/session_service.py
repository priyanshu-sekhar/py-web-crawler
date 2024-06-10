import aiohttp

from src.service.base_service import BaseService


class SessionService(BaseService):
    def __init__(self):
        self.session = None

    async def setup(self):
        """
        Sets the session with a custom user agent
        """
        try:
            custom_agent = "Priyanshu-Assignment-Crawler/1.0 <pri.patra@gmail.com>"
            self.session = aiohttp.ClientSession(headers={"User-Agent": custom_agent})
        except Exception as e:
            print(f"Error creating aiohttp session: {e}")

    async def terminate(self):
        if self.session:
            await self.session.close()

    async def get(self, url):
        return await self.session.get(url)
