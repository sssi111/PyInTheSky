import re
import aiohttp
import asyncio
import json
from datetime import datetime
from bs4 import BeautifulSoup, Tag
import os
import logging
from typing import List, Dict, Any

from real_estate_scraper.scrapers.base import BaseScraper
from real_estate_scraper.scrapers.parsers.yandex_realty_parser import YandexRealtyParser
from real_estate_scraper.data.data_manager import DataManager

logger = logging.getLogger(__name__)


class YandexRealtyScraper(BaseScraper):
    def __init__(self, output_file: str = "yandex_realty.json"):
        super().__init__()
        self.data_manager = DataManager(output_file)
        self.base_url = "https://realty.yandex.ru/moskva/snyat/kvartira/"

    async def scrape_page(self, page: int) -> List[Dict[str, Any]]:
        url = f"{self.base_url}?page={page}"
        html = await self.make_request(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        ads = YandexRealtyParser.parse_page(soup)
        
        new_ads = [ad for ad in ads if not self.data_manager.is_seen(ad["id"])]
        return new_ads

    async def scrape(self, pages: int = 5) -> List[Dict[str, Any]]:
        async with self:
            tasks = [self.scrape_page(page) for page in range(1, pages + 1)]
            results = await asyncio.gather(*tasks)
            new_ads = [ad for page_ads in results for ad in page_ads]
            
            if new_ads:
                self.data_manager.save_data(new_ads)
            
            return new_ads

    def load_existing_data(self):
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                try:
                    data = json.load(f)
                    self.seen_ads = {ad["id"] for ad in data}
                except json.JSONDecodeError:
                    logger.error(f"Error decoding JSON from {self.output_file}, starting with empty data.")
                    self.seen_ads = set()
        else:
            self.seen_ads = set()

    def get_text(self, element: Tag, selector: str):
        found = element.select_one(selector)
        text: str = found.text if found else ""
        return text.strip()

    async def save_data(self, new_ads):
        if not new_ads:
            return

        existing_data = []
        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                existing_data = json.load(f)

        updated_data = existing_data + new_ads

        with open(self.output_file, "w") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)

        self.seen_ads.update(ad["id"] for ad in new_ads)
        logger.info(f"Saved {len(new_ads)} new ads") 