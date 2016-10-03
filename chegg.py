#!/usr/bin/python3
import requests
import time
import os
import json

# TODO figure out how to get sessionid
# TODO figure out how to get Authorization key
# TODO sit down and actually plan this thing out...

HEADERS = {
    # "access_token": "",
    # "X-CHEGG-DEVICEID": "",
    # "X-CHEGG-SESSIONID": "",
    # "Authorization": "",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48B)",
    "host": "hub.chegg.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

TOKEN = None


def set_auth(username, password, auth_key):
    HEADERS["Authorization"] = auth_key
    TOKEN = get_new_token(username, password)
    HEADERS["access_token"] = TOKEN.access_token


class Token:
    def __init__(self, chegg_id, access_token, refresh_token, issued_at, expires_in):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.issued_at = issued_at
        self.expires_in = expires_in
        self.chegg_id = chegg_id

    def expired(self):
        current_time = time.time()
        expiration_time = self.issued_at + self.expires_in
        return expiration_time > current_time

    def refresh(self):
        url = "https://hub.chegg.com/oauth/refreshToken"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data, headers=HEADERS).json()
        print("res: " + str(response))

        self.access_token = response["access_token"]
        self.refresh_token = response["refresh_token"]
        self.expires_in = response["expires_in"]
        self.issued_at = response["issued_at"]

    def as_dict(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "issued_at": self.issued_at,
            "chegg_id": self.chegg_id
        }

    def write_to_file(self, filename):
        with open(filename, "w") as output_file:
            json.dump(self.as_dict(), output_file)


def get_new_token(username, password):
    """ Retrieves a token using the api """
    url = "https://hub.chegg.com/oauth/token"
    data = {
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(url, data=data, headers=HEADERS).json()
    return Token(
        access_token=response["access_token"],
        refresh_token=response["refresh_token"],
        issued_at=int(response["issued_at"]),
        expires_in=int(response["expires_in"]),
        chegg_id=response["chegg_id"]
    )


def get_token(filename):
    """ Looks for a token in a json token file """
    with open(filename, "r") as token_file:
        json_token = json.load(token_file)

    return Token(
        access_token=json_token["access_token"],
        refresh_token=json_token["refresh_token"],
        issued_at=int(json_token["issued_at"]),
        expires_in=int(json_token["expires_in"]),
        chegg_id=json_token["chegg_id"]
    )


class Book:
    def __init__(self, isbn13, title, authors, isbn10=None, isbn=None, edition=None):
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.isbn = isbn
        self.title = title
        self.edition = edition
        self.authors = authors


def get_book(isbn13):
    url = "https://hub.chegg.com/v1/book/" + str(isbn13)
    response = requests.get(url, headers=HEADERS).json()["result"]

    return Book(
        isbn13=response["isbn13"],
        isbn10=response["isbn10"],
        isbn=response["isbn"],
        title=response["title"],
        authors=response["authors"],
        edition=response["edition"]
    )


class Chapter:
    def __init__(self, id, name, book_isbn):
        self.id = id
        self.name = name
        self.book_isbn = book_isbn


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


class Problem:
    def __init__(self, id, name, has_solution, chapter_id, book_isbn, steps=[]):
        self.id = id
        self.name = name
        self.chapter_id = chapter_id
        self.book_isbn = book_isbn
        self.has_solution = has_solution == "true"
        self.steps = steps


def get_problems(chapter):
    url = "https://hub.chegg.com/v1/chapter/" + chapter.id + "/problems?limit=100&offset=0"
    response = requests.get(url, headers=HEADERS).json()

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


class Solution:
    def __init__(self):
        pass


def get_steps(problem):
    url = "https://hub.chegg.com/v1/tbs/_/solutions"

    json = {
        "action": "Access",
        "isbn13": problem.book_isbn,
        "problemId": problem.id,
        "userAgent": "Mobile"
    }

    # I must be missing some parameter. It never sends more than 1 step.
    # Sometimes it sends none

    response = requests.post(url, json=json, headers=HEADERS).json()
    print(response)
