class Problem:
    def __init__(self, id, name, has_solution, chapter_id, book_isbn, steps=[]):
        self.id = id
        self.name = name
        self.chapter_id = chapter_id
        self.book_isbn = book_isbn
        self.has_solution = has_solution == "true"
        self.steps = steps
