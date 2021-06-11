#!/usr/bin/env python


from bs4 import BeautifulSoup
import logging
import requests
import urllib
import re


class BookDepository:
    def __init__(self, author, title):
        self.book_formats = {"Paperback": 1, "Hardback": 2}
        self.languages = {"English": 123}

        self.set_format()
        self.set_language()

        self.author = author
        self.title = title
        self.price = ""
        self.book_url = ""

    def set_format(self, format="Paperback"):
        self.book_format = self.book_formats[format]

    def set_language(self, language="English"):
        self.language = self.languages[language]

    def get_price(self):
        search_term = urllib.parse.quote_plus(f"{self.author} {self.title}")

        url = f"https://www.bookdepository.com/search?searchTerm={search_term}&availability=1&searchLang={self.language}&format={self.book_format}"

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        price_regexp = re.compile("\d+\.\d+")

        if r.history:
            # We've been redirected to a single book
            sale_price = soup.find(class_="sale-price")

            price = sale_price.find(text=True)
            book_url = r.url
        else:
            book_item = soup.find(class_="book-item")

            # [TODO] Check the book we've found actually matches
            #        the author/title we've searched for

            if book_item:
                price = book_item.find(class_="price").find(text=True)

                href = book_item.find(class_="item-img").find("a").get("href")
                book_url = f"https://www.bookdepository.com{href}"
            else:
                logging.error(f"No price found for {self.author} {self.title}")
                return

        cleaned_price = price_regexp.search(price)

        if cleaned_price:
            self.price = cleaned_price.group()
        else:
            self.price = "0.00"

        self.book_url = book_url
