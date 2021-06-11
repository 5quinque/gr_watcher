#!/usr/bin/env python


from bs4 import BeautifulSoup
import logging
import requests
import urllib
from unidecode import unidecode
import re


class Waterstones:
    def __init__(self, author, title):
        self.book_formats = {"Paperback": 17, "Hardback": 16}
        self.book_format = None

        self.author = author
        self.title = title
        self.price = ""
        self.book_url = ""

    def set_format(self, format="Paperback"):
        self.book_format = self.book_formats[format]


    def get_price(self):
        search_term = urllib.parse.quote_plus(unidecode(f"{self.author} {self.title}"))

        url = f"https://www.waterstones.com/books/search/term/{search_term}/sort/price-asc"

        if self.book_format:
            url += f"/format/{self.book_format}"

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")

        price_regexp = re.compile("\d+\.\d+")

        book_item = soup.find(class_="book-preview")

        if book_item:
            price = book_item.find(class_="price").find(text=True)

            href = book_item.find(class_="title").get("href")
            book_url = f"https://www.waterstones.com{href}"
        else:
            logging.error(f"No price found for {self.author} {self.title}")
            return

        cleaned_price = price_regexp.search(price)

        if cleaned_price:
            self.price = cleaned_price.group()
        else:
            self.price = "0.00"

        self.book_url = book_url
