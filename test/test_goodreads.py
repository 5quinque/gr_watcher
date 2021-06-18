import pytest

from gr_watcher.goodreads import GoodReads

@pytest.fixture
def example_list_multiple_pages():
    return "https://www.goodreads.com/review/list/74698639-ryan?shelf=to-read"


def test_default_initial_values(example_list):
    good_reads = GoodReads(example_list)

    assert good_reads.to_read_url == example_list

def test_get_book_urls(example_list):
    good_reads = GoodReads(example_list)

    book_urls = good_reads.get_book_urls()

    assert book_urls

def test_get_book_urls_multiple_pages(example_list_multiple_pages):
    good_reads = GoodReads(example_list_multiple_pages)

    book_urls = good_reads.get_book_urls()

    assert book_urls

def test_get_to_read(example_list):
    good_reads = GoodReads(example_list)

    good_reads.get_to_read()

    assert good_reads.to_read_books