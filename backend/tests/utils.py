import re


def normalise_whitespace(html):
    """Function that helps normalise HTML input for comparisons in testing.

    There are small whitespace differences between the jinja2 output and the expected
    test output. Small whitespace differences don't affect rendering of HTML,
    so they are normalised for making testing simpler.
    1) Normalises any excessive whitespace between tags
    2) Normalises excessive whitespace inside tags

    Args:
        html: The HTML to be normalised.

    Returns:
        Normalised HTML.
    """
    html = re.sub(r'>\s+<', '> <', html)
    html = re.sub(r'(\s{2,})', ' ', html)
    return html.strip()
