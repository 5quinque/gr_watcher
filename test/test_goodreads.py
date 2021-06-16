import pytest

from gr_watcher.goodreads import GoodReads

@pytest.fixture
def example_list():
    return "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"


def test_default_initial_values(example_list):
    good_reads = GoodReads(example_list)

    assert good_reads.to_read_url == example_list
