#!/usr/bin/env python


from bs4 import BeautifulSoup
import logging
import requests
import urllib
from unidecode import unidecode
import re


class Bookshop:
    def __init__(self, author, title):
        self.label = None
        self.book_format = None

        self.search_url = ""

        self.author = author
        self.title = title
        self.price = 0.00
        self.href = None

        self.bookshop_base_url = ""
        self.search_url = ""
        self.search_term = urllib.parse.quote_plus(
            unidecode(f"{self.author} {self.title}")
        )

    def clean_price(self, price):
        price_regexp = re.compile(r"\d+\.\d+")
        cleaned_price = price_regexp.search(price)
        if cleaned_price:
            self.price = float(cleaned_price.group())

    def get_price_text(self, book_item):
        return book_item.find(class_="price").find(text=True)

    def get_book_url(self, book_item):
        return book_item.find(class_="title").get("href")

    def get_price(self):
        r = requests.get(self.search_url)

        soup = BeautifulSoup(r.content, "html.parser")

        if r.history:
            self.handle_redirect(soup, r)
            return

        book_item = self.get_book_item(soup)

        if book_item:
            price = self.get_price_text(book_item)
            self.clean_price(price)
            href = self.get_book_url(book_item)

            self.book_url = f"{self.bookshop_base_url}{href}"
        else:
            logging.error(
                f"No price found for {self.author} {self.title} - {self.search_url}"
            )
