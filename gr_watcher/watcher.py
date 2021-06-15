#!/usr/bin/env python

import logging
from prometheus_client import Gauge

from .book import Book
from .goodreads import GoodReads
from .bookshops.AbeBooks import AbeBooks
from .bookshops.BookDepository import BookDepository
from .bookshops.Waterstones import Waterstones
from .utils.bcolors import bcolors


class Watcher:
    def __init__(self, list_url, gauge=None):
        self.bookshops = [
            AbeBooks,
            BookDepository,
            Waterstones,
        ]

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

    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self, books):
        self.__books = []

        for book in books:
            book.shops = self.create_shops(book)
            self.__books.append(book)

    def create_shops(self, book):
        shops = []

        for shop_class in self.bookshops:
            shops.append(shop_class(book.author, book.title))

        return shops

    def get_books(self):
        self.books = []

        good_reads = GoodReads(self.list_url)
        good_reads.get_to_read()

        for book in good_reads.to_read_books:
            book = Book(book["author"], book["title"])
            book.shops = self.create_shops(book)

            self.books.append(book)

    def get_prices(self):
        for book in self.books:
            book.get_prices()

    def output_prices(self):
        for book in self.books:
            logging.info(
                f"{bcolors.OKGREEN}{book.shop.price}{bcolors.ENDC} [{book.shop.label}] {book.title} {book.author} - {book.shop.book_url}"
            )
            self.gauge.labels(book.title, book.author, book.shop.label).set(
                book.shop.price
            )
