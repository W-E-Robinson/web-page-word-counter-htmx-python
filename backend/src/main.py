import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse

from pymongo import MongoClient

from db.mongo import (
    UrlError,
    add_new_count,
    get_counts,
    update_page,
    update_display,
)
from libs.templating import counts_html, reset_html

logger = logging.getLogger(__name__)  # where is this used? = has relevance?
logging.basicConfig(level=logging.DEBUG)  # NOTE: environment variable this


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """A HTTP handler responding with HTMX HTML for word counts web page.

    Attributes:
        mongo_client: MongoDB client for storing word counts information.

    """

    def __init__(self, *args, mongo_client, **kwargs):
        self.mongo_client = mongo_client
        super().__init__(*args, **kwargs)

    def complete_response(self, http_code, content=None):
        """Method to add start tag to tag stack.

        Args:
            http_code (int): HTTP code.
            content (html): HTML to respond to requester.

        """
        http_code_message = f"HTTP status code: {http_code}"
        logging.error(http_code_message) if http_code > 400 else logging.info(
            http_code_message)

        self.send_response(http_code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers",
                         "HX-Request, HX-Current-URL, HX-Target")
        self.send_header(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

        if (content is not None):
            content_message = f"Completing response with content: {content}"
            logging.error(content_message) if http_code > 400 else logging.info(
                content_message)
            logging.info("Writing content to response")
            self.wfile.write(content)

    def do_OPTIONS(self):
        """Method to handle OPTIONS requests."""
        logging.info("OPTIONS request,\nHeaders:\n%s\n", str(self.headers))
        self.complete_response(204)

    def do_GET(self):
        """Method to handle GET requests."""
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))

        parsed_query = urlparse(str(self.path))
        path = parsed_query.path

        match path:
            case "/reset":
                try:
                    content = reset_html().encode("utf-8")
                    self.complete_response(200, content)
                    return
                except Exception as e:
                    error = f"Exception during rendering of reset_form_template: {
                        e}"
                    logging.error(error)
                    self.complete_response(500, error.encode("utf-8"))
                    return

            case "/count":
                query = unquote(parsed_query.query)
                url = query.replace("url=", "")

                pagination_index = url.find("&page=")
                isPaginationRequest = pagination_index != -1

                display_index = url.find("&display=")
                isDisplayRequest = display_index != -1

                # Add words information for new URL, or update pagination or display.
                # NOTE: consider HTTP methods of pagination and display.
                # NOTE: for pagi + disp, check url already in word counts = another common mongo function called here before each further interaction? = or do as part and save a mondgo request?
                if isPaginationRequest:
                    pagination_value = url[pagination_index +
                                           len("&page="): None]
                    url = url[None: pagination_index]
                    try:
                        update_page(url, int(pagination_value),
                                    self.mongo_client)
                    except UrlError as e:
                        error = f"UrlError during updating of page: {
                            e.message}"
                        logging.error(error)
                        self.complete_response(e.code, error.encode("utf-8"))
                        return
                    except Exception as e:
                        error = f"Exception during updating of page: {
                            e}"
                        logging.error(error)
                        self.complete_response(500, error.encode("utf-8"))
                        return
                elif isDisplayRequest:
                    display_value = url[display_index + len("&display="): None]
                    url = url[None: display_index]
                    try:
                        update_display(url, False if display_value ==
                                       "false" else True, self.mongo_client)
                    except UrlError as e:
                        error = f"UrlError during updating of display: {
                            e.message}"
                        logging.error(error)
                        self.complete_response(e.code, error.encode("utf-8"))
                        return
                    except Exception as e:
                        error = f"Exception during updating of display: {
                            e}"
                        logging.error(error)
                        self.complete_response(500, error.encode("utf-8"))
                        return
                else:
                    try:
                        add_new_count(url, self.mongo_client)
                    except UrlError as e:
                        error = f"UrlError during addition of new URL count: {
                            e.message}"
                        logging.error(error)
                        self.complete_response(e.code, error.encode("utf-8"))
                        return
                    except Exception as e:
                        error = f"Exception during addition of new URL count: {
                            e}"
                        logging.error(error)
                        self.complete_response(500, error.encode("utf-8"))
                        return

                # Return updated words information
                try:
                    word_counts = get_counts(self.mongo_client)
                    content = counts_html(word_counts).encode("utf-8")
                    self.complete_response(200, content)
                    return
                except UrlError as e:
                    error = f"UrlError during getting of all counts: {
                        e.message}"
                    logging.error(error)
                    self.complete_response(e.code, error.encode("utf-8"))
                    return
                except Exception as e:
                    error = f"Exception during getting of all counts: {
                        e}"
                    logging.error(error)
                    self.complete_response(500, error.encode("utf-8"))
                    return

            case _:
                content = b"Not Found"
                self.complete_response(404, content)


def run(mongo_client):
    """Function to run HTTP client.

    Args:
        mongo_client: MongoDB client.

    """
    def handler_with_mongo_client(*args, **kwargs):
        return HTTPRequestHandler(*args, mongo_client=mongo_client, **kwargs)
    # NOTE: environment variable this
    httpd = HTTPServer(("0.0.0.0", 8080), handler_with_mongo_client)

    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except OSError as e:
        logging.error(f"OSError during server running: {e}")
        raise
    except KeyboardInterrupt:
        logging.warning("Stopping server due to keyboard interruption")
    except Exception as e:
        logging.error(f"Unknown error during server running: {e}")
        raise
    finally:
        httpd.server_close()
        logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    logging.info("Initiating MongoDb client")
    # NOTE: environment variable this
    mongo_client = MongoClient(
        "mongodb://web-page-word-counter-mongodb:27017/")
    run(mongo_client)
