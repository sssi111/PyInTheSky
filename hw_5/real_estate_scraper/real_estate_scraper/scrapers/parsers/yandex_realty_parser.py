import re
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any, Optional

class YandexRealtyParser:
    @staticmethod
    def parse_page(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        ads = []
        for item in soup.select(".OffersSerpItem"):
            try:
                ad_data = YandexRealtyParser._parse_item(item)
                if ad_data:
                    ads.append(ad_data)
            except Exception as e:
                continue
        return ads

    @staticmethod
    def _parse_item(item: Tag) -> Optional[Dict[str, Any]]:
        try:
            link = item.find("a", class_="OffersSerpItem__link")
            if not link:
                return None

            href = link["href"]
            ad_id = re.search(r"offer/(\d+)", href)
            if not ad_id:
                return None

            description = YandexRealtyParser._get_text(item, ".OffersSerpItem__description")
            price = YandexRealtyParser._get_text(item, ".OffersSerpItem__price")
            url = "https://realty.yandex.ru" + href

            return {
                "id": ad_id.group(1),
                "price": price,
                "description": description,
                "url": url,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception:
            return None

    @staticmethod
    def _get_text(element: Tag, selector: str) -> str:
        found = element.select_one(selector)
        return found.text.strip() if found else "" 
