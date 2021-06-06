#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import urllib


class BookDepository:
    def __init__(self, book_title):
        self.book_formats = {"Paperback": 1, "Hardback": 2}
        self.languages = {"English": 123}

        self.set_format()
        self.set_language()

        self.book_title = book_title
        self.price = ""
        self.book_url = ""

    def set_format(self, format="Paperback"):
        self.book_format = self.book_formats[format]

    def set_language(self, language="English"):
        self.language = self.languages[language]

    def get_price(self):
        search_term = urllib.parse.quote_plus(self.book_title)

        url = f"https://www.bookdepository.com/search?searchTerm={search_term}&availability=1&searchLang={self.language}&format={self.book_format}"

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        if r.history:
            # We've been redirected to a single book
            sale_price = soup.find(class_="sale-price")

            price = sale_price.find(text=True).strip()
            book_url = r.url
        else:
            book_item = soup.find(class_="book-item")

            if book_item:
                price = book_item.find(class_="price").find(text=True).strip()
                href = book_item.find(class_="item-img").find("a").get("href")
                book_url = f"https://www.bookdepository.com{href}"
            else:
                print("No books found")
                return

        self.price = price
        self.book_url = book_url
