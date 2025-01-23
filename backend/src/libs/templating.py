from os import path

from jinja2 import Environment, FileSystemLoader

environment = Environment(
    loader=FileSystemLoader(
        path.join(path.dirname(__file__), "../assets/templates")),
    trim_blocks=True,
    lstrip_blocks=True
)
table_template = environment.get_template("table_template.html")
reset_form_template = environment.get_template("reset_form_template.html")
counts_template = environment.get_template("counts_template.html")


def reset_html():
    """Function that returns reset HTML for the URL input form.

    Returns:
        The reset form HTML.
    """
    return reset_form_template.render()


def counts_html(word_counts):
    """Function that returns the counts HTML.

    Args:
        word_counts: A list of word counts from MongoDB.

    Returns:
        The word counts HTML.
    """
    content_list = []
    for info in word_counts:
        table_content = table_template.render(
            display=info["display"],
            word_count=info["word_count"],
            columns=("Word", "Count"),
            rows=info["paginated_words_list"],
            url=info["url"],
            prev_page=(
                info["current_page"] - 1
                if info["current_page"] >= 2
                else None
            ),
            next_page=(
                info["current_page"] + 1
                if info["num_pages"] > info["current_page"]
                else None
            ),
        )
        content_list.append(table_content)

    return counts_template.render(content_list=content_list)
