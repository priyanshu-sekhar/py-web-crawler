import aiohttp


class SessionService:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        """
        Sets the session with a custom user agent
        """
        try:
            custom_agent = "Priyanshu-Assignment-Crawler/1.0 <pri.patra@gmail.com>"
            self.session = aiohttp.ClientSession(headers={"User-Agent": custom_agent})
        except Exception as e:
            print(f"Error creating aiohttp session: {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get(self, url):
        return await self.session.get(url)
