import string
from itertools import product
from os import path
from time import time

import requests

endpoint = 'http://localhost:8002/flags/'

flags_dir = path.dirname(__file__)
flags_dir = path.join(flags_dir, 'flags')


class FlagNotFound(Exception):
    pass


def download_flag(country):
    url = flag_url(country)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise FlagNotFound()
    return resp.content


def flag_url(country):
    url = f'{endpoint}/{country}/{country}.gif'
    return url


def save_flag(image, country):
    flag_path = path.join(flags_dir, f'{country}.gif')
    with open(flag_path, 'wb') as f:
        f.write(image)
    return flag_path


def generate_countries():
    for a, b in product(string.ascii_lowercase, string.ascii_lowercase):
        yield a + b


def download_all_flags():
    for country in generate_countries():
        try:
            image = download_flag(country)
        except FlagNotFound:
            yield f'Flag not found: {country}'
        else:
            path = save_flag(image, country)
            yield path


if __name__ == '__main__':
    elapsed = time()
    for result in download_all_flags():
        print(result)
    print(f'Total time: {time()-elapsed}s')
