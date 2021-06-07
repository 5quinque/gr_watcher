#!/usr/bin/env python

import logging
from importlib import resources

from GoodReads import GoodReads
from Books import Database
from BookDepository import BookDepository
from utils.bcolors import bcolors


def get_books(database):
    good_reads = GoodReads(
        "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    )

    # good_reads = GoodReads(
    #     "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"
    # )

    good_reads.get_to_read()

    for book in good_reads.to_read_books:
        database.add_book(book["author"], book["title"])


def get_prices(database):
    for author in database.get_authors():
        for book in author.books:
            book_title = f"{author.first_name} {author.last_name} {book.title}"

            book_depo = BookDepository(book_title)
            book_depo.get_price()
            database.add_price(book_depo.price, book, book_depo.book_url)


def print_prices(database):
    for author in database.get_authors():
        for book in author.books:
            book_title = f"{author.first_name} {author.last_name} {book.title}"

            for price in book.prices:
                logging.info(
                    f"{bcolors.OKGREEN}{price.price}{bcolors.ENDC} {book_title}"
                )


def main():
    database = Database()

    # # Add the GoodReads list to our database
    get_books(database)

    get_prices(database)

    print_prices(database)


if __name__ == "__main__":
    with resources.path("data", "gr_watcher.log") as log_filepath:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[logging.FileHandler(log_filepath), logging.StreamHandler()],
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    main()
