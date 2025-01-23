import math
import urllib.request

from libs.counting import count_information


class UrlError(Exception):
    """A general error for searched URL related issues.

    Args:
        message (str): Human readable string with brief description and the error.
        code (int): Error code.

    Attributes:
        message (str): Human readable string with brief description and the error
        code (int): Error code.

    """

    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)


def add_new_count(url, client):
    """Function to add new URL count information into MongoDB.

    Args:
        URL (str): URL that count information is added for.
        client: MongoDB client.

    Raises:
        UrlError: If error getting current searched URLs in MongoDB.
        UrlError: If URL has already been searched for.
        UrlError: If error fetching HTML for searched URL.
        UrlError: If error inserting count information into MongoDB.

    """
    counts_collection = client["local_database"]["counts_collection"]

    try:
        searched_urls = counts_collection.find({}, {'url': 1, '_id': 0})
    except Exception as err:
        raise UrlError(
            f"error getting searched URLs: {err}", 500)

    urls_list = [doc['url'] for doc in searched_urls]

    if url in urls_list:
        raise UrlError(
            f"already searched for analysis of URL: {url}",
            400)

    try:
        contents = urllib.request.urlopen(url).read()
    except urllib.error.URLError as err:
        raise UrlError(f"error fetching HTML for URL: {
            url}, err: {err.reason}", 500)

    count_info = count_information(contents.decode('utf-8'))
    info = {
        "url": url,
        "current_page": 1,
        "display": True,
        "num_pages": math.ceil(len(count_info["words_list"]) / 5),
        "paginated_words_list": count_info["words_list"][0:5],
    }
    info.update(count_info)

    try:
        counts_collection.insert_one(info)
    except Exception as err:
        raise UrlError(
            f"error inserting data for URL: {url}, err: {err}", 500)


def update_page(url, new_page, client):
    """Function to update page in MongoDB for a given URL.

    Args:
        url (str): URL that page is updated for.
        new_page (int): New page value that URL page is updated to.
        client: MongoDB client.

    Raises:
        UrlError: If error finding word count information for URL.
        UrlError: If error updating page value for URL in MongoDB.

    """
    counts_collection = client["local_database"]["counts_collection"]

    try:
        words_list = counts_collection.find_one(
            {"url": {"$eq": url}},
            {"words_list": 1},
        )["words_list"]
    except Exception as err:
        raise UrlError(
            f"error finding word count information for URL: {url}, err: {err}", 500)

    try:
        counts_collection.update_one(
            {"url": url},
            {"$set": {"current_page": new_page, "paginated_words_list": words_list[(
                new_page - 1) * 5: new_page * 5]}}
        )
    except Exception as err:
        raise UrlError(
            f"error updating page for URL: {url}, err: {err}", 500)


def update_display(url, display, client):
    """Function to update display property in MongoDB for a given URL.

    Args:
        url (str): URL that page is updated for.
        display (bool): Dictates if the table of word counts information is displayed.
        client: MongoDB client.

    Raises:
        UrlError: If error updating display value for URL in MongoDB.

    """
    counts_collection = client["local_database"]["counts_collection"]

    try:
        counts_collection.update_one(
            {"url": url},
            {"$set": {"display": display}},
        )
    except Exception as err:
        raise UrlError(
            f"error updating display value for URL: {url}, err: {err}", 500)


def get_counts(client):
    """Function to get all counts MongoDB.

    Args:
        client: MongoDB client.

    Returns:
        The information on all word counts in MongoDB count collection.

    Raises:
        UrlError: If error getting counts.

    """
    counts_collection = client["local_database"]["counts_collection"]

    try:
        word_counts = counts_collection.find(
            {},
            {
                "display": 1,
                "word_count": 1,
                "paginated_words_list": 1,
                "url": 1,
                "current_page": 1,
                "num_pages": 1,
            },
        )
    except Exception as err:
        raise UrlError(
            f"error getting all counts, err: {err}", 500)

    return word_counts
