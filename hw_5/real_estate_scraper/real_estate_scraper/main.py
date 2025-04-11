import asyncio
import logging
from real_estate_scraper.scrapers.yandex_realty import YandexRealtyScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    scraper = YandexRealtyScraper()
    try:
        ads = await scraper.scrape(pages=5)
        logger.info(f"Successfully scraped {len(ads)} ads")
    except Exception as e:
        logger.error(f"Error during scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 