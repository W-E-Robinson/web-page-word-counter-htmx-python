import re
from html.parser import HTMLParser


class Parser(HTMLParser):
    """A parser for taking in an HTML feed and collectin word count information.

    Attributes:
        word_count (int): The total word count in the HTML.
        words_list: A dictionary of words and number of occurences for each word.
        currently_opened_tags: A list stack of encountered HTML tags.
        accepted_html_tags: A non-exhaustive list of accepted HTML tags to count words within.

    """

    def __init__(self):
        super().__init__()
        self.word_count = 0
        self.words_list = {}
        self.currently_opened_tags = []
        self.accepted_html_tags = [
            "body",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "section",
            "address",
            "li",
            "ol",
            "ul",
            "p",
            "a",
            "abbr",
            "b",
            "em",
            "thead",
            "th",
            "tr",
            "tfoot",
            "button",
        ]

    def handle_starttag(self, tag, attrs):
        """Method to add start tag to tag stack."""
        self.currently_opened_tags.append(tag)

    def handle_endtag(self, tag):
        """Method to pop end tag from tag stack."""
        self.currently_opened_tags.pop(len(self.currently_opened_tags) - 1)

    def handle_data(self, data):
        """Method to analyse HTML and update self.words_list and self.word_count."""
        if self.currently_opened_tags.count("body") == 1 and self.accepted_html_tags.count(self.currently_opened_tags[len(self.currently_opened_tags) - 1]) == 1:
            data_list = re.split("\s", data)
            final_list = []
            for word in data_list:
                updated_word = re.sub("[.,!?]+$", "", word)
                if not re.search("[^a-zA-Z0-9]", updated_word) and updated_word != "":
                    final_list.append(updated_word.lower())

            for word in final_list:
                if word in self.words_list:
                    self.words_list[word] += 1
                else:
                    self.words_list[word] = 1

            self.word_count += len(final_list)


def count_information(html):
    """Function to return count information for a given HTML input.

    Args:
        html: HTML to be analysed for word count.

    Returns:
        Dictionary of word count information with: word_count, words_list.

    """
    parser = Parser()
    parser.feed(html)

    word_count = getattr(parser, 'word_count')
    words_list_dict = getattr(parser, 'words_list')

    words_list = []
    for key, value in words_list_dict.items():
        words_list.append([key, value])

    def sort_by_word_count(item):
        return item[1]

    words_list.sort(key=sort_by_word_count, reverse=True)

    return {
        "word_count": word_count,
        "words_list": words_list,
    }
