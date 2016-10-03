class Book:
    def __init__(self, isbn13, title, authors, isbn10=None, isbn=None, edition=None):
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.isbn = isbn
        self.title = title
        self.edition = edition
        self.authors = authors
