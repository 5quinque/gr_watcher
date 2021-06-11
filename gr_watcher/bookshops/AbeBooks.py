#!/usr/bin/env python


from bs4 import BeautifulSoup
import logging
import requests
import urllib
from unidecode import unidecode
import re


class AbeBooks:
    def __init__(self, author, title):
        self.author = author
        self.title = title
        self.price = ""
        self.book_url = ""

    def get_price(self):
        # unidecode because abebooks doesn't like accented characters
        search_author = urllib.parse.quote_plus(unidecode(self.author))
        search_title = urllib.parse.quote_plus(unidecode(self.title))

        url = f"https://www.abebooks.co.uk/servlet/SearchResults?an={search_author}&n=100121501&sortby=17&tn={search_title}"

        r = requests.get(url)

        soup = BeautifulSoup(r.content, "html.parser")
        price_regexp = re.compile("\d+\.\d+")

        book_item = soup.find(class_="result-item")

        if book_item:
            price = book_item.find(itemprop="price").get("content")
            href = book_item.find(itemprop="url").get("href")
            book_url = f"https://www.abebooks.co.uk{href}"
        else:
            logging.error(
                f"No price found for {self.title} - URL: {url} Status: {r.status_code}"
            )
            return

        cleaned_price = price_regexp.search(price)

        if cleaned_price:
            self.price = cleaned_price.group()
        else:
            self.price = "0.00"

        self.book_url = book_url
