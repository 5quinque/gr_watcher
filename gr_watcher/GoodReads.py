import aiohttp
import asyncio
import logging
import requests
from bs4 import BeautifulSoup


class GoodReads:
    def __init__(self, to_read_url):
        self.to_read_url = to_read_url
        self.to_read_books = []

        self.loop = asyncio.get_event_loop()
        self.tasks = []

    def get_book_urls(self):
        """May be multiple pages to a booklist, this method returns all page urls"""
        book_urls = [self.to_read_url]

        r = requests.get(self.to_read_url)
        soup = BeautifulSoup(r.content, "html.parser")

        pages = soup.find(id="reviewPagination")

        if pages is None:
            return book_urls

        for page in pages.find_all("a"):
            url = page.get("href")
            book_urls.append(f"https://www.goodreads.com{url}")

        # Convert to a set to get a unique list and return it
        return set(book_urls)

    def get_to_read(self):
        book_urls = self.get_book_urls()

        for url in book_urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            books = soup.find_all(class_="bookalike")
            self.get_books(books)

        self.loop.run_until_complete(asyncio.wait(self.tasks))

        for b in self.to_read_books:
            logging.debug(f"Found: {b['title']} {b['author']}")

    def get_books(self, books):
        for book in books:
            url = book.find(class_="title").find("a").get("href")

            task = asyncio.ensure_future(
                self.get_book_info(f"https://www.goodreads.com{url}")
            )
            self.tasks.append(task)

    async def get_book_info(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.read(), "html.parser")

                # isbn = soup.find(itemprop="isbn")
                # [TODO] Catch errors at this point
                author = soup.find(class_="authorName").find(itemprop="name")
                title = soup.find(id="bookTitle")

                # isbn = isbn.get_text().strip() if isbn else "ISBN Not Found"
                author = author.get_text().strip() if author else "Author Not Found"
                title = title.get_text().strip() if title else "Title Not Found"

                book_dict = {
                    # "isbn": isbn,
                    "title": title,
                    "author": author,
                    "url": url,
                }

                self.to_read_books.append(book_dict)
