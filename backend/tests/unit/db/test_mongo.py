import urllib.request
from unittest.mock import Mock, patch

import pytest

from db.mongo import (
    UrlError,
    add_new_count,
    get_counts,
    update_page,
    update_display,
)


def test_it_raises_when_an_error_arises_getting_searched_urls():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.side_effect = Exception("mongo error")

    url = "https://example.com"

    with pytest.raises(UrlError) as exc:
        add_new_count(url, mock_client)

    assert str(
        exc.value.message) == "error getting searched URLs: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


# NOTE: extract this logic into its own mongodb function, then can use with pagi and display to check url IS in mongodb
def test_it_raises_when_a_url_has_already_been_counted():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.return_value = [
        {"url": "https://example.com", "id": 0},
    ]

    url = "https://example.com"

    with pytest.raises(UrlError) as exc:
        add_new_count(url, mock_client)

    assert str(
        exc.value.message) == "already searched for analysis of URL: https://example.com"
    assert exc.value.code == 400

    assert isinstance(exc.value, UrlError)


def test_it_raises_when_error_searching_url():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.return_value = []

    url = "https://example.com"

    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("URL error")):
        with pytest.raises(UrlError) as exc:
            add_new_count(url, mock_client)

    assert str(
        exc.value.message) == "error fetching HTML for URL: https://example.com, err: URL error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


def test_it_raises_when_error_inserting_new_count():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.return_value = []
    mock_counts_collection.insert_one.side_effect = Exception("mongo error")

    url = "https://example.com"

    mock_response = Mock()
    mock_response.read = lambda: b"mock HTML"

    with patch("urllib.request.urlopen", return_value=mock_response):
        with patch("db.mongo.count_information", return_value={
            "word_count": 6,
            "words_list": [
                ['sample', 6],
            ],
        }):
            with pytest.raises(UrlError) as exc:
                add_new_count(url, mock_client)

    assert str(
        exc.value.message) == "error inserting data for URL: https://example.com, err: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


def test_it_adds_new_count():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.return_value = []
    mock_counts_collection.insert_one.return_value = None

    url = "https://example.com"

    mock_response = Mock()
    mock_response.read = lambda: b"mock HTML"

    with patch("urllib.request.urlopen", return_value=mock_response):
        with patch("db.mongo.count_information", return_value={
            "word_count": 6,
            "words_list": [
                ['sample', 6],
            ],
        }):
            add_new_count(url, mock_client)
            mock_counts_collection.insert_one.assert_called_once_with({
                "url": url,
                "current_page": 1,
                "display": True,
                "word_count": 6,
                "num_pages": 1,
                "paginated_words_list": [
                    ['sample', 6],
                ],
                "words_list": [
                    ['sample', 6],
                ],
            })


def test_it_raises_when_error_getting_words_list_for_doc_to_update():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find_one.side_effect = Exception("mongo error")

    url = "https://example.com"
    new_page = 2

    with pytest.raises(UrlError) as exc:
        update_page(url, new_page, mock_client)

    assert str(
        exc.value.message) == "error finding word count information for URL: https://example.com, err: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


def test_it_raises_when_error_updating_a_page():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find_one.return_value = {"words_list": [
        ["one", 5],
        ["two", 10],
        ["three", 5],
        ["four", 10],
        ["five", 5],
        ["six", 10],
    ]}
    mock_counts_collection.update_one.side_effect = Exception("mongo error")

    url = "https://example.com"
    new_page = 2

    with pytest.raises(UrlError) as exc:
        update_page(url, new_page, mock_client)

    assert str(
        exc.value.message) == "error updating page for URL: https://example.com, err: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


def test_it_updates_a_page():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find_one.return_value = {
        "words_list": [
            ["one", 5],
            ["two", 10],
            ["three", 5],
            ["four", 10],
            ["five", 5],
            ["six", 10],
        ]
    }
    mock_counts_collection.update_one.return_value = None

    url = "https://example.com"
    new_page = 2

    update_page(url, new_page, mock_client)

    mock_counts_collection.update_one.assert_called_once_with(
        {"url": url},
        {"$set": {"current_page": new_page,
                  "paginated_words_list": [["six", 10]]}}
    )


def test_it_raises_when_error_updating_display():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.update_one.side_effect = Exception("mongo error")

    url = "https://example.com"
    new_display = True

    with pytest.raises(UrlError) as exc:
        update_display(url, new_display, mock_client)

    assert str(
        exc.value.message) == "error updating display value for URL: https://example.com, err: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)


def test_it_updates_a_display():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.update_one.return_value = None

    url = "https://example.com"
    new_display = True

    update_display(url, new_display, mock_client)

    mock_counts_collection.update_one.assert_called_once_with(
        {"url": url},
        {"$set": {"display": True}},
    )


def test_it_raises_when_error_getting_all_counts():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.side_effect = Exception("mongo error")

    with pytest.raises(UrlError) as exc:
        get_counts(mock_client)

    assert str(
        exc.value.message) == "error getting all counts, err: mongo error"
    assert exc.value.code == 500

    assert isinstance(exc.value, UrlError)

    mock_client["local_database"]["counts_collection"].find.assert_called_once(
    )


def test_it_gets_all_counts():
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    mock_counts_collection = MagicMock()
    mock_client.__getitem__.return_value = {
        "counts_collection": mock_counts_collection
    }
    mock_counts_collection.find.return_value = [
        ["banana", 5],
        ["apple", 10],
    ]

    result = get_counts(mock_client)

    assert result == [["banana", 5], ["apple", 10]]

    mock_client["local_database"]["counts_collection"].find.assert_called_once(
    )
