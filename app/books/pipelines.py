import logging


from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class UniqueBooksPipeline:
    """An item pipeline to filter out duplicate books."""

    def __init__(self):
        self.seen_books = set()

    def process_item(self, item, spider):
        if item["upc"] in self.seen_books:
            raise DropItem(f"Seen book: {item['upc']}")

        logger.info(f"New book: {item['upc']}")
        self.seen_books.add(item["upc"])
        return item
