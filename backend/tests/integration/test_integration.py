import pytest
import requests
from pymongo import MongoClient

from utils import normalise_whitespace

# This will serve up /tests/fixtures/sample1.html
test_1_url = "http://sample-1-html-server:8080"
# This will serve up /tests/fixtures/sample2.html
test_2_url = "http://sample-2-html-server:8080"


mongo_client = MongoClient("mongodb://localhost:27017/")


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    """Function that removes all documents from the MongoDB counts_collection collection"""
    counts_collection = mongo_client["local_database"]["counts_collection"]
    counts_collection.delete_many({})


def test_it_responds_with_options():
    response = requests.options("http://localhost:8080")

    assert response.status_code == 204


def test_it_responds_with_reset_html():
    response = requests.get("http://localhost:8080/reset")

    assert response.status_code == 200
    assert response.content.decode("utf-8") == """<form id="form">
    <input type="text" name="url" value="">
    <button class="btn" hx-get="http://localhost:8080/reset" hx-trigger="click" hx-target="#form" hx-swap="outerHTML">
        Reset
    </button>
    <button class="btn" hx-get="http://localhost:8080/count" hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
        Count
    </button>
</form>"""


def test_it_responds_with_a_searched_count():
    response = requests.get(
        f"http://localhost:8080/count?url={test_1_url}")

    assert response.status_code == 200
    assert normalise_whitespace(response.content.decode("utf-8")) == normalise_whitespace("""<div id="counts">
    <div>
        <div>
            <h1>http://sample-1-html-server:8080 - 27</h1>
            <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <table>
            <tr>
                <th>Word</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>sample</td>
                <td>6</td>
            </tr>
            <tr>
                <td>text</td>
                <td>4</td>
            </tr>
            <tr>
                <td>html</td>
                <td>2</td>
            </tr>
            <tr>
                <td>1</td>
                <td>2</td>
            </tr>
            <tr>
                <td>welcome</td>
                <td>1</td>
            </tr>
            <tr>
                <td>
                    <button class="btn" disabled>
                        Previous DISABLED
                    </button>
                </td>
                <td>
                    <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&page=2"
                        hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                        Next
                    </button>
                </td>
            </tr>
        </table>
    </div>
</div>""")


def test_it_responds_with_multiple_searched_counts():
    requests.get(f"http://localhost:8080/count?url={test_1_url}")
    response = requests.get(f"http://localhost:8080/count?url={test_2_url}")

    assert response.status_code == 200
    assert normalise_whitespace(response.content.decode("utf-8")) == normalise_whitespace("""<div id="counts">
    <div>
        <div>
            <h1>http://sample-1-html-server:8080 - 27</h1>
            <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <table>
            <tr>
                <th>Word</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>sample</td>
                <td>6</td>
            </tr>
            <tr>
                <td>text</td>
                <td>4</td>
            </tr>
            <tr>
                <td>html</td>
                <td>2</td>
            </tr>
            <tr>
                <td>1</td>
                <td>2</td>
            </tr>
            <tr>
                <td>welcome</td>
                <td>1</td>
            </tr>
            <tr>
                <td>
                    <button class="btn" disabled>
                        Previous DISABLED
                    </button>
                </td>
                <td>
                    <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&page=2"
                        hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                        Next
                    </button>
                </td>
            </tr>
        </table>
    </div>
    <div>
        <div>
            <h1>http://sample-2-html-server:8080 - 28</h1>
            <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-2-html-server:8080&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <table>
            <tr>
                <th>Word</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>sample</td>
                <td>6</td>
            </tr>
            <tr>
                <td>additional</td>
                <td>4</td>
            </tr>
            <tr>
                <td>text</td>
                <td>4</td>
            </tr>
            <tr>
                <td>html</td>
                <td>2</td>
            </tr>
            <tr>
                <td>2</td>
                <td>2</td>
            </tr>
            <tr>
                <td>
                    <button class="btn" disabled>
                        Previous DISABLED
                    </button>
                </td>
                <td>
                    <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-2-html-server:8080&page=2"
                        hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                        Next
                    </button>
                </td>
            </tr>
        </table>
    </div>
</div>""")


def test_it_responds_with_updated_pagination():
    requests.get(f"http://localhost:8080/count?url={test_1_url}")
    response = requests.get(
        f"http://localhost:8080/count?url={test_1_url}&page=2")

    print(response.status_code)
    print(response.content)
    assert response.status_code == 200
    assert normalise_whitespace(response.content.decode("utf-8")) == normalise_whitespace("""<div id="counts">
    <div>
        <div>
            <h1>http://sample-1-html-server:8080 - 27</h1>
            <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <table>
            <tr>
                <th>Word</th>
                <th>Count</th>
            </tr>
            <tr>
                <td>to</td>
                <td>1</td>
            </tr>
            <tr>
                <td>this</td>
                <td>1</td>
            </tr>
            <tr>
                <td>is</td>
                <td>1</td>
            </tr>
            <tr>
                <td>the</td>
                <td>1</td>
            </tr>
            <tr>
                <td>content</td>
                <td>1</td>
            </tr>
            <tr>
                <td>
                    <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&page=1"
                        hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                        Previous
                    </button>
                </td>
                <td>
                    <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&page=3"
                        hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                        Next
                    </button>
                </td>
            </tr>
        </table>
    </div>
</div>""")


def test_it_responds_with_updated_display():
    requests.get(f"http://localhost:8080/count?url={test_1_url}")
    response = requests.get(
        f"http://localhost:8080/count?url={test_1_url}&display=false")

    assert response.status_code == 200
    assert normalise_whitespace(response.content.decode("utf-8")) == normalise_whitespace("""<div id="counts">
    <div>
        <div>
            <h1>http://sample-1-html-server:8080 - 27</h1>
            <button class="btn" hx-get="http://localhost:8080/count?url=http://sample-1-html-server:8080&display=true" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Open
            </button>
        </div>
    </div>
</div>""")


def test_it_responds_with_error_when_URL_already_searched():
    requests.get(f"http://localhost:8080/count?url={test_1_url}")
    response = requests.get(f"http://localhost:8080/count?url={test_1_url}")

    assert response.status_code == 400
    assert response.content.decode(
        "utf-8") == "Error during addition of new URL count: already searched for analysis of URL: http://sample-1-html-server:8080"


def test_it_responds_with_404_not_found():
    response = requests.get("http://localhost:8080/not-found")

    assert response.status_code == 404
    assert response.content.decode("utf-8") == "Not Found"
