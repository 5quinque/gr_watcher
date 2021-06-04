#!/usr/bin/env python


from GoodReads import GoodReads
from Books import Database


def main():
    database = Database()

    good_reads = GoodReads(
        "https://www.goodreads.com/review/list/74698639-ryan?per_page=100&shelf=to-read"
    )

    # good_reads = GoodReads(
    #     "https://www.goodreads.com/review/list/74698639-ryan?shelf=test"
    # )

    # good_reads.get_to_read()

    # for b in good_reads.to_read_books:
    #     database.add_new_book(b["author"], b["title"])

    for author in database.get_authors():
        print(author.first_name, author.last_name)
        for book in author.books:
            print("  ", book.title)


if __name__ == "__main__":
    main()
