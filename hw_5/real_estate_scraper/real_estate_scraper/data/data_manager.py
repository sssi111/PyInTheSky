import json
import os
import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.seen_ids: Set[str] = set()
        self.load_existing_data()

    def load_existing_data(self) -> None:
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.seen_ids = {item["id"] for item in data}
            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON from {self.output_file}")
                self.seen_ids = set()
        else:
            self.seen_ids = set()

    def save_data(self, new_items: List[Dict[str, Any]]) -> None:
        if not new_items:
            return

        existing_data = []
        if os.path.exists(self.output_file):
            with open(self.output_file, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    logger.error(f"Error reading existing data from {self.output_file}")

        updated_data = existing_data + new_items

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)

        self.seen_ids.update(item["id"] for item in new_items)
        logger.info(f"Saved {len(new_items)} new items")

    def is_seen(self, item_id: str) -> bool:
        return item_id in self.seen_ids
