import pytest

from gr_watcher.bookshops.BookDepository import BookDepository

@pytest.fixture
def author():
    return "Nicholson Baker"

@pytest.fixture
def book_title():
    return "The Mezzanine"


def test_default_initial_values(author, book_title):
    bookdepo = BookDepository(author, book_title)

    assert bookdepo.author == author
    assert bookdepo.title == book_title


def test_get_price(author, book_title):
    bookdepo = BookDepository(author, book_title)

    bookdepo.get_price()

    assert type(bookdepo.price) is float
    assert bookdepo.price > 0.00

def test_set_format(author, book_title):
    bookdepo = BookDepository(author, book_title)
    bookdepo.set_format("Paperback")

    bookdepo.get_price()

    assert type(bookdepo.price) is float
    assert bookdepo.price > 0.00

def test_set_language(author, book_title):
    bookdepo = BookDepository(author, book_title)
    bookdepo.set_language("English")

    bookdepo.get_price()

    assert type(bookdepo.price) is float
    assert bookdepo.price > 0.00