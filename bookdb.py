# -*- coding: utf-8 -*-
"""
Created on Mon July  6 13:16:00 2020

@author: Anders J. Andersen
"""

import sqlite3

books_db = "books.db"


def get_books():
    """
    Reads all books from books table order by book id

    :return: List of books
    :rtype: List of book rows as tuples or None
    """
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from books order by id")
        return curs.fetchall()


def get_book(pid: int):
    """
    Reads one row from books table with the provided id

    :param pid:Book id
    :type pid:int
    :return: A row of data from books table
    :rtype: a book row as a tuple or None
    """
    if not isinstance(pid, int):
        raise Exception("Book id has an invalid type, must be an integer")
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from books where id = ?", (pid,))
        return curs.fetchone()


def get_publisher(pid: int):
    """
    Reads one publisher from publishers table with the provided id

    :param pid: Publisher Id
    :type pid: int
    :return: A row of data from publishers table
    :rtype: a publisher row as a tuple or None
    """
    if not isinstance(pid, int):
        raise Exception("Publisher id has an invalid type, must be an integer")
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from publishers where id = ?", (pid,))
        return curs.fetchone()


def get_author(pid: int):
    """
    Reads an author from authors table with the provided id

    :param pid: Author Id
    :type pid: int
    :return: A row of data from authors table
    :rtype: a author row as a tuple or None
    """
    if not isinstance(pid, int):
        raise Exception("Author id has an invalid type, must be an integer")
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from authors where id = ?", (pid,))
        return curs.fetchone()


def save_book(
    pid: int | None,
    authors: list[int],
    publisher: int,
    isbn: str,
    edition: str,
    title: str,
):
    """
    Saves a new book or update an existing book.
    A new book is created if the value of pid is None.
    If the value of pid is an integer the book with that id is updated

    :param pid: Book id
    :type pid: None or int
    :param author: Author id
    :type author: int
    :param publisher: Publisher id
    :type publisher: int
    :param isbn: The books ISBN number
    :type isbn: str
    :param edition: The edition of the book
    :type edition: str
    :param title: The title of the book
    :type title: str
    :return: Result of insert or update
    :rtype: bool
    """
    result = False
    try:
        if pid is None:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute(
                    "insert into books (publisher, isbn, edition, title) values (?, ?, ?, ?) returning id",
                    (publisher, isbn, edition, title),
                )
                pid = curs.lastrowid
                if pid is not None:
                    save_bookaothors(con, pid, authors)
                con.commit()
                result = True
        else:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute(
                    """update books set
                                publisher = :pub,
                                isbn = :isbn,
                                edition = :edt,
                                title = :title
                                where id = :id""",
                    {
                        "pub": publisher,
                        "isbn": isbn,
                        "edt": edition,
                        "title": title,
                        "id": pid,
                    },
                )
                save_bookaothors(con, pid, authors)
                con.commit()
                result = True
    except Exception as e:
        print(f"Error in save_book: {e}")
        result = False
    return result


def save_bookaothors(con, bookid: int, authors: list[int]):
    delete_bookauthors(con, bookid)
    sql = "insert into book_authors (bookid, authorid) values (?, ?)"
    for authorid in authors:
        curs = con.cursor()
        curs.execute(sql, (bookid, authorid))


def delete_bookauthors(con, bookid: int):
    sql = "delete from book_authors where bookid = ? "
    curs = con.cursor()
    curs.execute(sql, (bookid,))


def get_book_authors(pid):
    sql = """select a.id, a.name from book_authors ba
            join authors a on a.id = ba.authorid
            where ba.bookid = :bookid"""
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute(sql, {"bookid": pid})
        return curs.fetchall()


def save_publisher(pid: int | None, name: str):
    """
    Saves a new publisher or update an existing one.
    A new publisher is created if the value of pid is None.
    If the value of pid is an integer the publisher with that id is updated

    :param pid: The publisher id
    :type pid: None or int
    :param name: The name of the publisher
    :type name: str
    :return: Result of insert or update
    :rtype: bool
    """
    result = False
    try:
        if pid is None:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute("insert into publishers (name) values (?)", (name,))
                con.commit()
                result = True
        else:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute(
                    """update publishers
                                set name = :name
                                where id = :id""",
                    {"name": name, "id": pid},
                )
                con.commit()
                result = True
    except Exception as e:
        print(f"Error in save_publisher: {e}")
        result = False
    return result


def save_author(pid: int | None, name: str):
    """

    :param pid: The author id
    :type pid: None or int
    :param name: The name of the author
    :type name: str
    :return: Result of insert or update
    :rtype: bool
    """
    result = False
    try:
        if pid is None:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute("insert into authors (name) values (?)", (name,))
                con.commit()
                result = True
        else:
            with sqlite3.connect(books_db) as con:
                curs = con.cursor()
                curs.execute(
                    """update authors
                                set name = :name
                                where id = :id""",
                    {"name": name, "id": pid},
                )
                con.commit()
                result = True
    except Exception as e:
        print(f"Error in save_author: {e}")
        result = False
    return result


def delete_book(book_id: int):
    """

    :param book_id: The book id
    :type book_id: int
    """
    if book_id is not None:
        with sqlite3.connect(books_db) as con:
            curs = con.cursor()
            curs.execute("delete from books where id = :id", {"id": book_id})
            curs.execute("delete from book_authors where bookid = :id", {"id": book_id})
            con.commit()


def delete_publisher(publisher_id: int):
    """

    :param publisher_id: The publisher id
    :type publisher_id: int
    """
    if not isinstance(publisher_id, int):
        raise Exception("publisher_id has an invalid type, must be an integer")
    if publisher_id is not None:
        with sqlite3.connect(books_db) as con:
            curs = con.cursor()
            curs.execute("delete from publishers where id = :id", {"id": publisher_id})
            con.commit()


def delete_author(author_id: int):
    """

    :param author_id: The author id
    :type author_id: int
    """
    if not isinstance(author_id, int):
        raise Exception("author_id has an invalid type, must be an integer")
    if author_id is not None:
        with sqlite3.connect(books_db) as con:
            curs = con.cursor()
            curs.execute("delete from authors where id = :id", {"id": author_id})
            con.commit()


def get_authors():
    """

    :return: List of authors
    :rtype: list of author rows as tuples
    """
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from authors")
        return curs.fetchall()


def get_publishers():
    """

    :return: List of publishers
    :rtype: list of publisher rows as tuples
    """
    with sqlite3.connect(books_db) as con:
        curs = con.cursor()
        curs.execute("select * from publishers")
        return curs.fetchall()
