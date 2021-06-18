import pytest
import random
import string
from prometheus_client import Gauge

from gr_watcher.book import Book
from gr_watcher.watcher import Watcher


@pytest.fixture
def example_gauge():
    return Gauge(
        "".join(random.choices(string.ascii_uppercase, k=10)),
        "Description of gauge",
        ["title", "author", "bookshop"],
    )


@pytest.fixture
def books():
    return [
        Book("John Fowles", "The Collector"),
        Book("John Burnside", "The Dumb House"),
        Book("Cormac McCarthy", "The Road"),
        Book("Nicholson Baker", "The Mezzanine"),
    ]


def test_default_initial_values(example_list, example_gauge):
    watcher = Watcher(example_list, example_gauge)

    assert watcher.list_url == example_list

def test_gauge_none(example_list):
    watcher = Watcher(example_list)

    assert watcher.gauge


def test_get_books(example_list, example_gauge):
    watcher = Watcher(example_list, example_gauge)
    watcher.get_books()

    assert watcher.books


def test_get_prices(example_list, example_gauge, books):
    watcher = Watcher(example_list, example_gauge)
    watcher.books = books
    watcher.get_prices()

    for book in watcher.books:
        assert book.shop.price

def test_output_prices(example_list, example_gauge, books):
    watcher = Watcher(example_list, example_gauge)
    watcher.books = books
    watcher.get_prices()

    watcher.output_prices()

