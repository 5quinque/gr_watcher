import pytest

from gr_watcher.bookshops.AbeBooks import AbeBooks
from gr_watcher.bookshops.BookDepository import BookDepository
from gr_watcher.bookshops.Waterstones import Waterstones

@pytest.fixture
def non_author():
    return "UUTWKTHNJZ"

@pytest.fixture
def non_book_title():
    return "O7UA7FOZFH"

@pytest.fixture
def bookshops():
    return [
            AbeBooks,
            BookDepository,
            Waterstones,
        ]

def test_default_initial_values(bookshops, author, book_title):
    for shop in bookshops:
        shop_object = shop(author, book_title)

        assert shop_object.author == author
        assert shop_object.title == book_title


def test_get_price(bookshops, author, book_title):
    for shop in bookshops:
        shop_object = shop(author, book_title)

        shop_object.get_price()

        assert type(shop_object.price) is float
        assert shop_object.price > 0.00

def test_nonexistent_book(bookshops, non_author, non_book_title):
    for shop in bookshops:
        shop_object = shop(non_author, non_book_title)

        shop_object.get_price()

        assert shop_object.href == None
        assert shop_object.price == 0.00