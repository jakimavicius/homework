from concurrent import futures
import logging

import grpc

from protocols import parser_pb2
from protocols import parser_pb2_grpc

from parsel import Selector


class ParserService(parser_pb2_grpc.ParserServicer):
    def ParseBookPage(self, request, context):
        print(f"Got request to parse: {request.url}")
        data = parse_book_page(request)
        if data:
            result = parser_pb2.BookResult(is_valid=True, data=data)
        else:
            result = parser_pb2.BookResult(is_valid=False)
        return result


def parse_book_page(page: parser_pb2.Page) -> parser_pb2.BookData | None:
    selector = Selector(page.html)

    # Extract book title, if present.
    name = selector.css(".product_page h1::text").get()

    if not name:
        return None

    data = {"name": name}

    # Extract book details from information table
    for row in selector.css(".table > tr"):
        field = row.css("th::text").get()
        match field:
            case "UPC":
                data["upc"] = row.css("td::text").get()
            case "Availability":
                data["availability"] = row.css("td::text").get()
            case "Price (excl. tax)":
                data["price_excl_tax"] = row.css("td::text").get()
            case "Tax":
                data["tax"] = row.css("td::text").get()

    return parser_pb2.BookData(**data)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    parser_pb2_grpc.add_ParserServicer_to_server(ParserService(), server)
    server.add_insecure_port(
        f"[::]:{port}"
    )  # Listen on port 50051 (insecure for simplicity)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
