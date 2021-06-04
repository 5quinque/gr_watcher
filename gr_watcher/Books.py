#!/usr/bin/env python

from sqlalchemy import (
    and_,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    MetaData,
)
from sqlalchemy.orm import Session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


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


class Database:
    def __init__(self, dbname="books.db"):
        self.engine = create_engine(f"sqlite:///{dbname}")

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
        try:
            metadata.create_all(self.engine)
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def add_new_book(self, author_name, book_title):
        """Adds a new book to the system"""
        # Get the author's first and last names
        first_name, _, last_name = author_name.partition(" ")

        # Check if book exists
        book = (
            self.session.query(Book)
            .join(Author)
            .filter(Book.title == book_title)
            .filter(
                and_(Author.first_name == first_name, Author.last_name == last_name)
            )
            .one_or_none()
        )
        # Does the book by the author already exist?
        if book is not None:
            return

        # Create the book
        book = Book(title=book_title)

        # Get the author
        author = (
            self.session.query(Author)
            .filter(
                and_(Author.first_name == first_name, Author.last_name == last_name)
            )
            .one_or_none()
        )
        # Do we need to create the author?
        if author is None:
            author = Author(first_name=first_name, last_name=last_name)
            self.session.add(author)

        # Initialize the book relationships
        book.author = author
        self.session.add(book)

        # Commit to the database
        self.session.commit()

    def get_authors(self):
        """Get a list of author objects sorted by last name"""
        return self.session.query(Author).order_by(Author.last_name).all()
