#!/usr/bin/env python

from sqlalchemy import (
    and_,
    create_engine,
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Table,
    MetaData,
)
from sqlalchemy.orm import Session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from importlib import resources
import datetime

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book", backref=backref("author"))


class Book(Base):
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    title = Column(String)
    prices = relationship("Price", backref=backref("book"))


class Price(Base):
    __tablename__ = "price"
    price_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.book_id"))
    price = Column(String)
    shop_url = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Database:
    def __init__(self, dbname="author_book_price.db"):
        with resources.path("data", dbname) as sqlite_filepath:
            self.engine = create_engine(f"sqlite:///{sqlite_filepath}")

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        # Attempt to create tables
        self.create_db_tables()

    def create_db_tables(self):
        metadata = MetaData()
        authors = Table(
            "author",
            metadata,
            Column("author_id", Integer, primary_key=True),
            Column("first_name", String),
            Column("last_name", String),
        )
        books = Table(
            "book",
            metadata,
            Column("book_id", Integer, primary_key=True),
            Column("author_id", Integer, ForeignKey("author.author_id")),
            Column("title", String),
        )
        prices = Table(
            "price",
            metadata,
            Column("price_id", Integer, primary_key=True),
            Column("book_id", Integer, ForeignKey("book.book_id")),
            Column("price", String),
            Column("shop_url", String),
            Column("created_date", DateTime, default=datetime.datetime.utcnow),
        )
        try:
            metadata.create_all(self.engine)
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def get_author(self, author_name):
        first_name, _, last_name = author_name.partition(" ")

        author = (
            self.session.query(Author)
            .filter(
                and_(Author.first_name == first_name, Author.last_name == last_name)
            )
            .one_or_none()
        )

        return author

    def get_book(self, book_title, author_name):
        first_name, _, last_name = author_name.partition(" ")

        book = (
            self.session.query(Book)
            .join(Author)
            .filter(Book.title == book_title)
            .filter(
                and_(Author.first_name == first_name, Author.last_name == last_name)
            )
            .one_or_none()
        )

        return book

    def add_book(self, author_name, book_title):
        """Adds a new book to the system"""
        # Get the author's first and last names
        first_name, _, last_name = author_name.partition(" ")

        book = self.get_book(book_title, author_name)

        # Does the book by the author already exist?
        if book is not None:
            return

        # Create the book
        book = Book(title=book_title)

        author = self.get_author(author_name)

        # Do we need to create the author?
        if author is None:
            author = Author(first_name=first_name, last_name=last_name)
            self.session.add(author)

        # Initialize the book relationships
        book.author = author
        self.session.add(book)

        # Commit to the database
        self.session.commit()

    def add_price(self, price, book, shop_url):
        # [TODO] Compare with latest price and only add a new record if different
        price = Price(price=price, book_id=book.book_id, shop_url=shop_url)
        self.session.add(price)

        # Commit to the database
        self.session.commit()

    def get_authors(self):
        """Get a list of author objects sorted by last name"""
        return self.session.query(Author).order_by(Author.last_name).all()
