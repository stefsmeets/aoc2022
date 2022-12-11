import time


def timeit(func):
    def wrapper(*args, **kw):

        t0 = time.time()
        result = func(*args, **kw)
        t1 = time.time()

        print(f'> {func.__name__} took: {t1-t0:.3f} s, result: {result}')

        return result

    return wrapper


def get_year_and_day() -> tuple[int, int]:
    from pathlib import Path

    cwd = Path.cwd()
    day_s = cwd.name
    year_s = cwd.parent.name

    try:
        day, year = int(day_s.strip('day')), int(year_s.strip('aoc'))
    except ValueError:
        raise ValueError(f'Cannot get day/year from working dir: {cwd}')

    return year, day


def get_headers(year: int) -> dict[str, str]:
    from cookie import cookie
    return {
        'Cookie': cookie,
        'User-Agent': f'https://github.com/stefsmeets/aoc{year} by Stef Smeets'
    }


def download(day: int, year: int) -> str:
    import requests

    url = f'https://adventofcode.com/{year}/day/{day}/input'

    headers = get_headers(year=year)
    r = requests.get(url, headers=headers)

    return r.text


def download_entry():
    year, day = get_year_and_day()

    s = download(day=day, year=year)

    with open('data.txt', 'w') as f:
        f.writelines(s)

    lines = s.splitlines()

    for i, line in enumerate(lines):
        if len(line) > 80:
            print(f'{line[:75]} ...')
        else:
            print(line)

        if i == 10:
            print('...')
            break


def remove_tags(text: str) -> str:
    from xml.etree import ElementTree
    return ''.join(ElementTree.fromstring(text).itertext())


def submit(answer: int, part: int, day: int, year: int):
    import re
    import requests

    re_ANSWER = re.compile(r'<article>(<p>.*?</p>)')

    url = f'https://adventofcode.com/{year}/day/{day}/answer'

    data = {'level': part, 'answer': answer}

    headers = get_headers(year=year)
    r = requests.post(url, headers=headers, data=data)

    match = re_ANSWER.search(r.text)
    if match:
        print(remove_tags(match[1]))
    else:
        # Unexpected output
        print(r.text)


def submit_entry():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--part', type=int, choices=(1, 2))
    parser.add_argument('-a', '--answer', type=int)
    args = parser.parse_args()

    year, day = get_year_and_day()

    submit(
        answer=args.answer,
        part=args.part,
        day=day,
        year=year,
    )
