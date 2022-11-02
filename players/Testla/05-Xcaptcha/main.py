import re
import requests


def main() -> None:
    url = 'http://202.38.93.111:10047/?token=<Redacted>'
    captcha_url = 'http://202.38.93.111:10047/xcaptcha'
    with requests.Session() as s:
        r = s.get(url)
        # print(r.status_code)
        # print(r.text)
        r = s.get(captcha_url)
        print(r.status_code)
        print(r.text)
        results = []
        data = {}
        for i in range(1, 3 + 1):
            match = re.search(f'captcha{i}">([^ ]+) ', r.text)
            results.append(eval(match.group(1)))
            data[f'captcha{i}'] = eval(match.group(1))
        print(results)
        r = s.post(captcha_url, data=data)
        print(r.status_code)
        print(r.text)


if __name__ == "__main__":
    main()
