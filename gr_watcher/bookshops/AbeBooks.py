#!/usr/bin/env python

import urllib
from unidecode import unidecode

from .Bookshop import Bookshop


class AbeBooks(Bookshop):
    def __init__(self, author, title):
        super().__init__(author, title)

        self.label = "abebooks"

        search_author = urllib.parse.quote_plus(unidecode(self.author))
        search_title = urllib.parse.quote_plus(unidecode(self.title))

        self.bookshop_base_url = "https://www.abebooks.co.uk"
        self.search_url = f"https://www.abebooks.co.uk/servlet/SearchResults?an={search_author}&n=100121501&sortby=17&tn={search_title}"

    def get_book_item(self, soup):
        return soup.find(class_="result-item")

    def get_book_url(self, book_item):
        return book_item.find(itemprop="url").get("href")

    def get_price_text(self, book_item):
        return book_item.find(itemprop="price").get("content")
