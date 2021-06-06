#!/usr/bin/env python

from GoodReads import GoodReads
from Books import Database
from BookDepository import BookDepository
from utils.bcolors import bcolors

def get_books(database):
    # good_reads = GoodReads(
    #     "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    # )

    good_reads = GoodReads(
        "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"
    )

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

            print(book_title)
            for price in book.prices:
                print(f"{bcolors.OKGREEN}{price.price}{bcolors.ENDC}")


def main():
    database = Database()

    # # Add the GoodReads list to our database
    # get_books(database)

    # get_prices(database)

    print_prices(database)


if __name__ == "__main__":
    main()
