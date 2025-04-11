import aiohttp
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def scrape_page(self, page: int) -> list:
        pass

    @abstractmethod
    async def scrape(self, pages: int = 5) -> list:
        pass

    async def make_request(self, url: str, timeout: int = 10) -> str:
        try:
            async with self.session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Error {response.status} for URL: {url}")
                    return ""
        except Exception as e:
            logger.error(f"Request failed for URL {url}: {e}")
            return "" 