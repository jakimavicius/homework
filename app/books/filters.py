import logging

from itemadapter import ItemAdapter


logger = logging.getLogger(__name__)


class UniqueBookFilter:
    """Custom item filter to ensure only unique books are kept."""

    def __init__(self, feed_options):
        self.feed_options = feed_options
        self.seen_books = set()  # used to track already seen books.

    def accepts(self, item):
        item = ItemAdapter(item)

        if "upc" in item and item["upc"] not in self.seen_books:
            self.seen_books.add(item["upc"])
            logger.info(f"New book: {item['upc']}")
            return True

        logger.debug(f"Seen book: {item['upc']}")
        return False
