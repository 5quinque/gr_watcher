#!/usr/bin/env python

import logging
from importlib import resources
from prometheus_client import start_http_server, Gauge
import time

from GoodReads import GoodReads

from bookshops.AbeBooks import AbeBooks
from bookshops.BookDepository import BookDepository
from bookshops.Bookshop import Bookshop
from utils.bcolors import bcolors


class Watcher:
    def __init__(self, list_url):
        # self.database = Database()
        self.list_url = list_url
        self.books = []

        self.gauge = Gauge(
            "goodreads_list1",
            "Description of gauge",
            ["title", "author", "bookshop"],
        )

    def get_books(self):
        self.books = []

        good_reads = GoodReads(self.list_url)
        good_reads.get_to_read()

        for book in good_reads.to_read_books:
            # self.database.add_book(book["author"], book["title"])
            self.books.append({"author": book["author"], "title": book["title"]})

    def get_prices(self):
        for book in self.books:
            abe_books = AbeBooks(author=book["author"], title=book["title"])
            abe_books.get_price()
            if abe_books.price:
                self.gauge.labels(book["title"], book["author"], "abebooks").set(
                    abe_books.price
                )
                logging.info(
                    f"{bcolors.OKGREEN}{abe_books.price}{bcolors.ENDC} [abebooks] {book['title']} {book['author']}"
                )

            book_depo = BookDepository(author=book["author"], title=book["title"])
            book_depo.get_price()
            if book_depo.price:
                self.gauge.labels(book["title"], book["author"], "bookdepository").set(
                    book_depo.price
                )
                logging.info(
                    f"{bcolors.OKGREEN}{book_depo.price}{bcolors.ENDC} [bookdepository] {book['title']} {book['author']}"
                )


def main():
    # Start up the server to expose the metrics.
    start_http_server(5000, addr="0.0.0.0")

    list = (
        "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    )
    # list = "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"

    watcher = Watcher(list)

    while True:
        watcher.get_books()
        watcher.get_prices()

        time.sleep(3000)

    # watcher.print_prices()


if __name__ == "__main__":
    with resources.path("data", "gr_watcher.log") as log_filepath:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.FileHandler(log_filepath), logging.StreamHandler()],
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    main()
