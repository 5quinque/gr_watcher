#!/usr/bin/env python

import logging
from importlib import resources
from prometheus_client import start_http_server, Gauge
import time

from GoodReads import GoodReads

from bookshops.AbeBooks import AbeBooks
from bookshops.BookDepository import BookDepository
from bookshops.Bookshop import Bookshop
from bookshops.Waterstones import Waterstones
from utils.bcolors import bcolors


class Watcher:
    def __init__(self, list_url):
        self.bookshops = {
            "abebooks": AbeBooks,
            "bookdepository": BookDepository,
            "waterstones": Waterstones,
        }

        self.list_url = list_url
        self.books = []

        self.gauge = Gauge(
            "goodreads_list1",
            "Description of gauge",
            ["title", "author", "bookshop"],
        )

    def create_shops(self, book):
        shops = {}

        for shop, shop_class in self.bookshops.items():
            shops[shop] = shop_class(book["title"], book["author"])

        return shops

    def get_books(self):
        self.books = []

        good_reads = GoodReads(self.list_url)
        good_reads.get_to_read()

        for book in good_reads.to_read_books:
            book = {"author": book["author"], "title": book["title"]}
            book["shops"] = self.create_shops(book)
            self.books.append(book)

    def get_prices(self):
        for book in self.books:
            for shop, shop_object in book["shops"].items():
                self.get_shop_price(shop_object, shop, book)

    def get_shop_price(self, shop_object, shop_label, book):
        shop_object.get_price()
        if shop_object.price:
            self.gauge.labels(book["title"], book["author"], shop_label).set(
                shop_object.price
            )
            logging.info(
                f"{bcolors.OKGREEN}{shop_object.price}{bcolors.ENDC} [{shop_label}] {book['title']} {book['author']}"
            )


def main():
    # Start up the server to expose the metrics.
    start_http_server(5000, addr="0.0.0.0")

    # list = (
    #     "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    # )
    list = "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"

    watcher = Watcher(list)

    while True:
        watcher.get_books()
        watcher.get_prices()

        time.sleep(3000)


if __name__ == "__main__":
    with resources.path("data", "gr_watcher.log") as log_filepath:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.FileHandler(log_filepath), logging.StreamHandler()],
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    main()
