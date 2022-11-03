import sys
import re

import httpx


def main(url):
    client = httpx.Client()
    client.get(url, follow_redirects=True)

    url = httpx.URL(url).copy_with(path="/xcaptcha", query=None)

    page = client.get(url)
    pattern = re.compile(r"<label for=\"(captcha\d)\">\s*(\d+)\+(\d+)\s*的结果是")
    data = {}
    for match in re.finditer(pattern, page.text):
        data[match.group(1)] = int(match.group(2)) + int(match.group(3))

    res = client.post(url, data=data)
    print(res.text)


if __name__ == "__main__":
    main(sys.argv[1])
