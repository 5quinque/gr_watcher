#!/usr/bin/env python


from GoodReads import GoodReads
from Books import Database
from BookDepository import BookDepository


def main():
    database = Database()

    good_reads = GoodReads(
        "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    )

    # good_reads = GoodReads(
    #     "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"
    # )

    good_reads.get_to_read()

    for b in good_reads.to_read_books:
        database.add_book(b["author"], b["title"])

    for author in database.get_authors():
        for book in author.books:
            book_title = f"{author.first_name} {author.last_name} {book.title}"

            book_depo = BookDepository(book_title)
            book_depo.get_price()

            book = database.get_book(
                book.title, f"{author.first_name} {author.last_name}"
            )

            database.add_price(book_depo.price, book, book_depo.book_url)

            print(book_title)
            print(book_depo.price)
            print(book_depo.book_url)
            print()


if __name__ == "__main__":
    main()
