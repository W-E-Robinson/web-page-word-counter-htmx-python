from pathlib import Path

from libs.counting import count_information


def test_it_returns_the_correct_count_information():
    current_dir = Path(__file__).resolve().parent

    with open(current_dir / '../' / '../' / 'fixtures' / 'sample1.html', 'r') as file:
        sample_html = file.read()
    assert count_information(sample_html) == {
        "word_count": 27,
        "words_list": [
            ['sample', 6],
            ['text', 4],
            ['html', 2],
            ['1', 2],
            ['welcome', 1],
            ['to', 1],
            ['this', 1],
            ['is', 1],
            ['the', 1],
            ['content', 1],
            ['of', 1],
            ['it', 1],
            ['contains', 1],
            ['some', 1],
            ['for', 1],
            ['testing', 1],
            ['purposes', 1],
        ]
    }
