CREATE TABLE books (
    isbn13 INTEGER PRIMARY KEY,
    isbn10 INTEGER,
    isbn INTEGER,
    title VARCHAR NOT NULL,
    edition VARCHAR,
    author VARCHAR NOT NULL,
    ean VARCHAR,
    ebook_ean VARCHAR
);

CREATE TABLE chapters (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    book_isbn13 INTEGER NOT NULL,
    FOREIGN KEY(book_isbn13) REFERENCES books(isbn13)
);

CREATE TABLE problems (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    has_solution BOOLEAN NOT NULL,
    chapter_id INTEGER NOT NULL,
    FOREIGN KEY(chapter_id) REFERENCES chapters(id)
);

CREATE TABLE steps (
    id INTEGER PRIMARY KEY,
    type VARCHAR NOT NULL,
    num INTEGER NOT NULL,
    location VARCHAR NOT NULL,
    problem_id INTEGER NOT NULL,
    FOREIGN KEY(problem_id) REFERENCES problems(id)
);
