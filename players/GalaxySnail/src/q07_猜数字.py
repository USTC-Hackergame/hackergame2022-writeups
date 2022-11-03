import sys

import httpx


def init_client(token):
    headers = {"authorization": f"Bearer {token}"}
    client = httpx.Client(headers=headers)
    return client


def post_state(client: httpx.Client, url, guess):
    headers = {"Content-Type": "text/plain; charset=UTF-8"}
    content = f"<state><guess>{guess}</guess></state>"
    return client.post(url, headers=headers, content=content)


def main(token):
    client = init_client(token)
    url = "http://202.38.93.111:18000/state"
    post_state(client, url, "NaN")


if __name__ == "__main__":
    main(sys.argv[1])
