#!/usr/bin/env python


from .Bookshop import Bookshop


class BookDepository(Bookshop):
    def __init__(self, author, title):
        super().__init__(author, title)

        self.label = "bookdepository"

        self.book_formats = {"Paperback": 1, "Hardback": 2}
        self.languages = {"English": 123, "French": 137}

        self.bookshop_base_url = "https://www.bookdepository.com"
        self.search_url = f"https://www.bookdepository.com/search?searchTerm={self.search_term}&availability=1&searchSortBy=price_low_high"

    def set_format(self, format):
        self.search_url += f"&format={self.book_formats[format]}"

    def set_language(self, language):
        self.search_url += f"&searchLang={self.languages[language]}"

    def get_book_item(self, soup):
        return soup.find(class_="book-item")

    def get_book_url(self, book_item):
        return book_item.find(class_="item-img").find("a").get("href")

    def handle_redirect(self, soup, r):
        self.price = soup.find(class_="sale-price").find(text=True)
        self.clean_price()
        self.book_url = r.url
