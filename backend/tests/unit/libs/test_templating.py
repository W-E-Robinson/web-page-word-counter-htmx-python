from libs.templating import counts_html, reset_html
from utils import normalise_whitespace


def test_reset_html():
    assert normalise_whitespace(reset_html()) == normalise_whitespace("""<form id="form">
    <input type="text" name="url" value="">
    <button hx-get="http://localhost:8080/reset" hx-trigger="click" hx-target="#form" hx-swap="outerHTML">
        Reset
    </button>
    <button hx-get="http://localhost:8080/count" hx-trigger="click" hx-target="#counts"
        hx-swap="outerHTML" hx-include="[name='url']">
        Count
    </button>
</form>""")


def test_counts_html():
    # Second page is hidden and third page is paginated
    word_counts = [
        {
            "word_count": 12,
            "paginated_words_list": [
                ['sample', 6],
                ['text', 4],
                ['html', 2],
            ],
            "current_page": 1,
            "num_pages": 1,
            "url": "https://www.sample1.com",
            "display": True,
        },
        {
            "word_count": 1,
            "paginated_words_list": [
                ['html', 1],
            ],
            "current_page": 1,
            "num_pages": 1,
            "url": "https://www.sample2.com",
            "display": False,
        },
        {
            "word_count": 31,
            "paginated_words_list": [
                ['banana', 7],
                ['cherry', 6],
                ['test', 6],
                ['sample', 6],
                ['text', 4],
            ],
            "current_page": 1,
            "num_pages": 2,
            "url": "https://www.sample3.com",
            "display": True,
        }
    ]

    assert normalise_whitespace(counts_html(word_counts)) == normalise_whitespace("""<div id="counts">
    <div>
        <div class="url-header">
            <h4>https://www.sample1.com - 12</h4>
            <button class="counts-button" hx-get="http://localhost:8080/count?url=https://www.sample1.com&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <div class="count-table">
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
                    <td>
                        <button class="counts-button" disabled>
                            Previous
                        </button>
                    </td>
                    <td>
                        <button class="counts-button" disabled>
                            Next
                        </button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div>
        <div class="url-header">
            <h4>https://www.sample2.com - 1</h4>
            <button class="counts-button" hx-get="http://localhost:8080/count?url=https://www.sample2.com&display=true" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Open
            </button>
        </div>
    </div>
    <div>
        <div class="url-header">
            <h4>https://www.sample3.com - 31</h4>
            <button class="counts-button" hx-get="http://localhost:8080/count?url=https://www.sample3.com&display=false" hx-trigger="click"
                hx-target="#counts" hx-swap="outerHTML">
                Close
            </button>
        </div>
        <div class="count-table">
            <table>
                <tr>
                    <th>Word</th>
                    <th>Count</th>
                </tr>
                <tr>
                    <td>banana</td>
                    <td>7</td>
                </tr>
                <tr>
                    <td>cherry</td>
                    <td>6</td>
                </tr>
                <tr>
                    <td>test</td>
                    <td>6</td>
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
                    <td>
                        <button class="counts-button" disabled>
                            Previous
                        </button>
                    </td>
                    <td>
                        <button class="counts-button" hx-get="http://localhost:8080/count?url=https://www.sample3.com&page=2"
                            hx-trigger="click" hx-target="#counts" hx-swap="outerHTML">
                            Next
                        </button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</div>""")
