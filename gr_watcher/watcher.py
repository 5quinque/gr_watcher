#!/usr/bin/env python

import logging
from prometheus_client import Gauge

from .GoodReads import GoodReads
from .bookshops.AbeBooks import AbeBooks
from .bookshops.BookDepository import BookDepository
from .bookshops.Waterstones import Waterstones
from .utils.bcolors import bcolors


class Watcher:
    def __init__(self, list_url, gauge=None):
        self.bookshops = {
            "abebooks": AbeBooks,
            "bookdepository": BookDepository,
            "waterstones": Waterstones,
        }

        self.list_url = list_url
        self.books = []

        if gauge is None:
            self.gauge = Gauge(
                "goodreads_list1",
                "Description of gauge",
                ["title", "author", "bookshop"],
            )
        else:
            self.gauge = gauge

    def create_shops(self, book):
        shops = {}

        for shop, shop_class in self.bookshops.items():
            shops[shop] = shop_class(book["author"], book["title"])

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
            best_shop_object = None
            best_shop = None

            for shop, shop_object in book["shops"].items():
                shop_object.get_price()
                if (
                    best_shop_object is None
                    or shop_object.price < best_shop_object.price
                ):
                    best_shop_object = shop_object
                    best_shop = shop

            logging.info(
                f"{bcolors.OKGREEN}{best_shop_object.price}{bcolors.ENDC} [{best_shop}] {book['title']} {book['author']} - {best_shop_object.book_url}"
            )
            self.gauge.labels(book["title"], book["author"], best_shop).set(
                best_shop_object.price
            )

