#!/usr/bin/python3
import os
import sqlite3
import chegg

DB_LOC = "books.db"


def insert_book(book):
    db_connection = sqlite3.connect(DB_LOC)
    db_cursor = db_connection.cursor()

    query_string = "insert into books (isbn13, isbn10, isbn, title, edition, author) values (?, ?, ?, ?, ?, ?)"
    book_data = (book.isbn13, book.isbn10, book.isbn, book.title, book.edition, book.authors[0])
    db_cursor.execute(query_string, book_data)

    db_connection.commit()
    db_connection.close()


def insert_chapters(chapters):
    db_connection = sqlite3.connect(DB_LOC)
    db_cursor = db_connection.cursor()

    chapter_lists = []
    for chapter in chapters:
        chapter_lists += [(chapter.id, chapter.name, chapter.book_isbn)]

    query_string = "insert into chapters (id, name, book_isbn13) values (?, ?, ?)"
    db_cursor.executemany(query_string, chapter_lists)

    db_connection.commit()
    db_connection.close()


def insert_problems(problems):
    db_connection = sqlite3.connect(DB_LOC)
    db_cursor = db_connection.cursor()

    problem_lists = []
    for problem in problems:
        problem_lists += [(problem.id, problem.name, problem.has_solution, problem.chapter_id)]

    query_string = "insert into problems (id, name, has_solution, chapter_id) values (?, ?, ?, ?)"
    db_cursor.executemany(query_string, problem_lists)

    db_connection.commit()
    db_connection.close()


def main():
    chegg.set_auth()

    print("Getting book")
    isbn = 9781118539712
    book = chegg.get_book(isbn)
    # insert_book(book)

    print("Getting chapters")
    chapters = chegg.get_chapters(book.isbn13)
    # insert_chapters(chapters)

    problems = {}
    print("Getting problems for chapter: ")
    for chapter in chapters:
        print(chapter.name)
        p = chegg.get_problems(chapter)
        # insert_problems(p)
        problems[chapter.name] = p

if __name__ == "__main__":
    main()
