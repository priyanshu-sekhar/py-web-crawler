import aiofiles


class FileIO:
    def __init__(self, file_name):
        self.file_name = file_name

    async def write_to_file(self, url):
        async with aiofiles.open(self.file_name, "a") as f:
            await f.write(url + "\n")
