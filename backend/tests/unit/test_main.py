from unittest.mock import MagicMock, patch

from main import HTTPRequestHandler
from db.mongo import UrlError


class TestableHTTPRequestHandler(HTTPRequestHandler):
    def __init__(self):
        self.send_header = MagicMock()
        self.end_headers = MagicMock()
        self.send_response = MagicMock()
        self.wfile = MagicMock()
        self.requestline = "request line"
        self.client_address = "client address"
        self.request_version = "1"
        self.headers = {}
        self.mongo_client = {}


def test_it_completes_response_with_no_content():
    handler = TestableHTTPRequestHandler()

    handler.complete_response(200)

    handler.send_response.assert_called_once_with(200)
    handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
    handler.send_header.assert_any_call(
        "Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header.assert_any_call(
        "Cache-Control", "no-cache, no-store, must-revalidate")
    handler.end_headers.assert_called_once()


def test_it_completes_response_with_content():
    handler = TestableHTTPRequestHandler()

    content = "content".encode("utf-8")
    handler.complete_response(200, content)

    handler.send_response.assert_called_once_with(200)
    handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
    handler.send_header.assert_any_call(
        "Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header.assert_any_call(
        "Cache-Control", "no-cache, no-store, must-revalidate")
    handler.end_headers.assert_called_once()
    handler.wfile.write.assert_called_once_with(content)


def test_it_responds_with_options():
    handler = TestableHTTPRequestHandler()

    handler.do_OPTIONS()

    handler.send_response.assert_called_once_with(204)
    handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
    handler.send_header.assert_any_call(
        "Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header.assert_any_call(
        "Cache-Control", "no-cache, no-store, must-revalidate")
    handler.end_headers.assert_called_once()


def test_it_responds_with_error_html_when_reset_templating_exception_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/reset"

    with patch("main.reset_html", side_effect=Exception("reset template error")):
        handler.do_GET()

        error = "Error during rendering of reset_form_template: reset template error".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_reset_html():
    handler = TestableHTTPRequestHandler()

    handler.path = "/reset"
    result = "<div>mock reset template</div>"

    with patch("main.reset_html", return_value=result):
        handler.do_GET()

        handler.send_response.assert_called_once_with(200)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(result.encode("utf-8"))


def test_it_responds_with_error_html_when_add_new_count_url_error_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com"

    with patch("main.add_new_count", side_effect=UrlError("URL error", 400)):
        handler.do_GET()

        error = "Error during addition of new URL count: URL error".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(400)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_add_new_count_exception_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com"

    with patch("main.add_new_count", side_effect=Exception("exception")):
        handler.do_GET()

        error = "Error during addition of new URL count: exception".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_update_page_url_error_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com&page=2"

    with patch("main.update_page", side_effect=UrlError("URL error", 500)):
        handler.do_GET()

        error = "Error during updating of page: URL error".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_update_page_exception_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com&page=2"

    with patch("main.update_page", side_effect=Exception("exception")):
        handler.do_GET()

        error = "Error during updating of page: exception".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_update_display_url_error_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com&display=true"

    with patch("main.update_display", side_effect=UrlError("URL error", 500)):
        handler.do_GET()

        error = "Error during updating of display: URL error".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_update_display_exception_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com&display=true"

    with patch("main.update_display", side_effect=Exception("exception")):
        handler.do_GET()

        error = "Error during updating of display: exception".encode(
            "utf-8")

        handler.send_response.assert_called_once_with(500)
        handler.send_header.assert_any_call("Access-Control-Allow-Origin", "*")
        handler.send_header.assert_any_call(
            "Access-Control-Allow-Methods", "GET, OPTIONS")
        handler.send_header.assert_any_call(
            "Cache-Control", "no-cache, no-store, must-revalidate")
        handler.end_headers.assert_called_once()
        handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_get_counts_url_error_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com"

    with patch("main.add_new_count"):
        with patch("main.get_counts", side_effect=UrlError("URL error", 500)):
            handler.do_GET()

            error = "Error during getting of all counts: URL error".encode(
                "utf-8")

            handler.send_response.assert_called_once_with(500)
            handler.send_header.assert_any_call(
                "Access-Control-Allow-Origin", "*")
            handler.send_header.assert_any_call(
                "Access-Control-Allow-Methods", "GET, OPTIONS")
            handler.send_header.assert_any_call(
                "Cache-Control", "no-cache, no-store, must-revalidate")
            handler.end_headers.assert_called_once()
            handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_error_html_when_get_counts_exception_occurs():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com"

    with patch("main.add_new_count"):
        with patch("main.get_counts", side_effect=Exception("exception")):
            handler.do_GET()

            error = "Error during getting of all counts: exception".encode(
                "utf-8")

            handler.send_response.assert_called_once_with(500)
            handler.send_header.assert_any_call(
                "Access-Control-Allow-Origin", "*")
            handler.send_header.assert_any_call(
                "Access-Control-Allow-Methods", "GET, OPTIONS")
            handler.send_header.assert_any_call(
                "Cache-Control", "no-cache, no-store, must-revalidate")
            handler.end_headers.assert_called_once()
            handler.wfile.write.assert_called_once_with(error)


def test_it_responds_with_counts_html():
    handler = TestableHTTPRequestHandler()

    handler.path = "/count?url=https://www.example.com"
    result = "<div>mock counts</div>"

    with patch("main.add_new_count"):
        with patch("main.get_counts"):
            with patch("main.counts_html", return_value=result):
                handler.do_GET()

                handler.send_response.assert_called_once_with(200)
                handler.send_header.assert_any_call(
                    "Access-Control-Allow-Origin", "*")
                handler.send_header.assert_any_call(
                    "Access-Control-Allow-Methods", "GET, OPTIONS")
                handler.send_header.assert_any_call(
                    "Cache-Control", "no-cache, no-store, must-revalidate")
                handler.end_headers.assert_called_once()
                handler.wfile.write.assert_called_once_with(
                    result.encode("utf-8"))


def test_it_responds_with_error_html_when_404_not_found():
    handler = TestableHTTPRequestHandler()

    handler.path = "/invalid-path"

    handler.do_GET()

    handler.send_response.assert_called_once_with(404)
    handler.send_header.assert_any_call(
        "Access-Control-Allow-Origin", "*")
    handler.send_header.assert_any_call(
        "Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header.assert_any_call(
        "Cache-Control", "no-cache, no-store, must-revalidate")
    handler.end_headers.assert_called_once()
    handler.wfile.write.assert_called_once_with("Not Found".encode("utf-8"))
