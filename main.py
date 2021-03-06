import argparse
import os
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def shorten_link(link, headers):
    payload = {"long_url": link}
    url = "https://api-ssl.bitly.com/v4/bitlinks"

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_click(bitlink, headers):
    payload = {"unit": "day", "units": -1}
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    total_clicks = response.json()["total_clicks"]
    return total_clicks


def is_bitlink(link, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}"
    response = requests.get(url, headers=headers)
    return response.ok
   

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.environ['BITLY_TOKEN']
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('link', nargs='?')
    namespace = parser.parse_args()
    if namespace.link:
        user_input = namespace.link
    else:
        user_input = input("Введите ссылку:\n")

    parse_link = urlsplit(user_input)
    user_link = parse_link.netloc + parse_link.path

    if is_bitlink(user_link, HEADERS):
        try:
            clicks_count = count_click(user_link, HEADERS)
        except requests.exceptions.HTTPError:
            print("Неправильный битлинк")
        else:
            print(f"По вашей ссылке прошли: {clicks_count} раз(а)")
    else:
        try:
            bitlink = shorten_link(user_input, HEADERS)
        except requests.exceptions.HTTPError:
            print("Неправильная ссылка")
        else:
            print('Битлинк', bitlink)
