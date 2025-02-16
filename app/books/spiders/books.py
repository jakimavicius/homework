import grpc
import scrapy

from books.items import BookItem
from protocols import parser_pb2
from protocols import parser_pb2_grpc


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    default_start_url = (
        "https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html"
    )

    def start_requests(self):
        """Custom implementation to respect START_URL setting."""
        return [scrapy.Request(self.settings.get("START_URL", self.default_start_url))]

    async def parse(self, response):
        """Parse response by going to book page or following next page link."""

        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

        books = response.css("article.product_pod")
        for book in books:
            url = response.urljoin(book.css("h3 > a::attr(href)").get())
            yield scrapy.Request(url, callback=self.parse_book_details)

    async def parse_book_details(self, response):
        """Extract book data from a book details page."""
        grpc_parser_address = self.settings.get("GRPC_PARSER_ADDRESS")
        with grpc.insecure_channel(
            grpc_parser_address
        ) as channel:  # Connect to the server (insecure for simplicity)
            stub = parser_pb2_grpc.ParserStub(channel)  # Create the client stub
            page = parser_pb2.Page(url=response.url, html=response.text)
            resp = stub.ParseBookPage(page)

            if resp.is_valid:
                fields = ("name", "availability", "upc", "price_excl_tax", "tax")
                data = {field: getattr(resp.data, field) for field in fields}
                yield BookItem(**data)
