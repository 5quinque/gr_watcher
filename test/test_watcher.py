import pytest
from prometheus_client import Gauge

from gr_watcher.watcher import Watcher


@pytest.fixture
def example_list():
    return "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"

@pytest.fixture
def example_gauge():
    return Gauge(
        "test_gauge",
        "Description of gauge",
        ["title", "author", "bookshop"],
    )

def test_default_initial_values(example_list):
    watcher = Watcher(example_list, example_gauge)

    assert watcher.list_url == example_list

def test_get_books(example_list, example_gauge):
    watcher = Watcher(example_list, example_gauge)
    watcher.get_books()

    assert watcher.books

