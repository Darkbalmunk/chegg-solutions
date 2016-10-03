#!/usr/bin/python3
import requests
from models import (Token, Book, Chapter, Problem, Solution)


# TODO figure out how to get sessionid
# TODO figure out how to get Authorization key


class Chegg:

    def __init__(self, username, password, auth):

        self.headers = {
            "Authorization": auth,
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48B)",
            "host": "hub.chegg.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

        self.token = Token(username, password, self.headers)

    def requires_token(func):
        pass

    def get_book(self, isbn13):
        url = "https://hub.chegg.com/v1/book/" + str(isbn13)
        response = requests.get(url, headers=self.headers).json()["result"]

        return Book(
            isbn13=response["isbn13"],
            isbn10=response["isbn10"],
            isbn=response["isbn"],
            title=response["title"],
            authors=response["authors"],
            edition=response["edition"]
        )

    def get_chapters(self, isbn):
        url = "https://hub.chegg.com/v1/book/" + str(isbn) + "/chapters?limit=100&offset=0"

        response = requests.get(url, headers=self.headers).json()

        chapters = []

        for json_chapter in response["result"]:
            chapter = Chapter(
                id=json_chapter["id"],
                name=json_chapter["name"],
                book_isbn=isbn
            )
            chapters += [chapter]
        return chapters

    def get_problems(self, chapter):
        url = "https://hub.chegg.com/v1/chapter/" + chapter.id + "/problems?limit=100&offset=0"
        response = requests.get(url, headers=self.headers).json()

        problems = []

        for json_problem in response["result"]:
            problem = Problem(
                id=json_problem["id"],
                name=json_problem["name"],
                chapter_id=json_problem["chapter"],
                has_solution=json_problem["hasSolution"] == "True",
                book_isbn=chapter.book_isbn
            )
            problems += [problem]
        return problems

    def get_solutions(self, problem):
        url = "https://hub.chegg.com/v1/tbs/_/solutions"

        data = {
            "action": "Access",
            "isbn13": problem.book_isbn,
            "problemId": problem.id,
            "userAgent": "Mobile"
        }

        # I must be missing some parameter. It never sends more than 1 step.
        # Sometimes it sends none

        response = requests.post(url, json=data, headers=self.headers).json()
        print(response)
