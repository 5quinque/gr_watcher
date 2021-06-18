import pytest

@pytest.fixture
def example_list():
    return "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"

@pytest.fixture
def author():
    return "Nicholson Baker"

@pytest.fixture
def book_title():
    return "The Mezzanine"

