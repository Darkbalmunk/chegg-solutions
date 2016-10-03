import json
import time
import requests


class Token:
    def __init__(self, username, password, headers=None):
        """ Retrieves a token using the api """
        url = "https://hub.chegg.com/oauth/token"
        data = {
            "username": username,
            "password": password,
            "grant_type": "password"
        }

        response = requests.post(url, data=data, headers=headers).json()

        self.access_token = response["access_token"],
        self.refresh_token = response["refresh_token"],
        self.issued_at = int(response["issued_at"]),
        self.expires_in = int(response["expires_in"]),
        self.chegg_id = response["chegg_id"]

    def expired(self):
        current_time = time.time()
        expiration_time = self.issued_at + self.expires_in
        return expiration_time > current_time

    def refresh(self, headers=None):
        url = "https://hub.chegg.com/oauth/refreshToken"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data, headers=headers).json()
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
