#!/usr/bin/python3
import requests

# TODO figure out how to get access token and sessionid
#   - I'm assuming device id is constant
# TODO verify that Authorization is constant

HEADERS = {
    "access_token": "",
    "X-CHEGG-DEVICEID": "",
    "X-CHEGG-SESSIONID": "",
    "Authorization": "",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48B)",
    "host": "hub.chegg.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}


class Chapter:

    def __init__(self, id, name, book_isbn, solutions=[]):
        self.solutions = []
        self.id = id
        self.name = name
        self.book_isbn = book_isbn


class Solution:

    def __init__(self, id, name, has_solution, chapter_id, book_isbn, steps=[]):
        self.id = id
        self.name = name
        self.chapter_id = chapter_id
        self.book_isbn = book_isbn
        self.has_solution = has_solution
        self.steps = steps


def get_chapters(isbn):
    url = "https://hub.chegg.com/v1/book/" + str(isbn) + "/chapters?limit=100&offset=0"

    response = requests.get(url, headers=HEADERS).json()

    chapters = []

    for json_chapter in response["result"]:
        chapter = Chapter(
            id=json_chapter["id"],
            name=json_chapter["name"],
            book_isbn=isbn
        )
        chapters += [chapter]

    return chapters


def get_solutions(chapter):
    url = "https://hub.chegg.com/v1/chapter/" + chapter.id + "/problems?limit=100&offset=0"
    response = requests.get(url, headers=HEADERS).json()

    solutions = []

    for json_solution in response["result"]:
        solution = Solution(
            id=json_solution["id"],
            name=json_solution["name"],
            chapter_id=json_solution["chapter"],
            has_solution=json_solution["hasSolution"] == "True",
            book_isbn=chapter.book_isbn
        )
        solutions += [solution]

    return solutions


def get_steps(solution):
    url = "https://hub.chegg.com/v1/tbs/_/solutions"

    data = {
        "action": "Access",
        "isbn13": solution.book_isbn,
        "problemId": solution.id,
        "userAgent": "Mobile"
    }

    response = requests.post(url, data=data, headers=HEADERS).json()
    print(response)


def main():
    isbn = 9781118539712
    chapters = get_chapters(isbn)
    solutions = get_solutions(chapters[0])
    get_steps(solutions[0])


if __name__ == "__main__":
    main()
