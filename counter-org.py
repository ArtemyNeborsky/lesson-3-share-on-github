import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def shorten_link(token, link):
    url = "https://api.vk.ru/method/"
    method_name = "utils.getShortLink"
    payload = {"access_token": token, "v": "5.199", "url": link}
    response = requests.get(url + method_name, params=payload)
    response.raise_for_status()
    return response.json()['response']["short_url"]


def count_clicks(token, ready_url):
    url = "https://api.vk.ru/method/"
    method_name = "utils.getLinkStats"
    key = urlparse(ready_url).path[1:]
    payload = {"access_token": token, "key": key, "interval": "forever", "v": "5.199"}
    response = requests.get(url + method_name, params=payload)
    response.raise_for_status()
    clicks_count = response.json()['response']["stats"][0]["views"]
    return clicks_count


def is_shorten_link(ready_url):
    url = "https://api.vk.ru/method/"
    method_name = "utils.getLinkStats"
    key = urlparse(ready_url).path[1:]
    payload = {"access_token": token, "key": key, "v": "5.199"}
    response = requests.get(url + method_name, params=payload)
    response.raise_for_status()
    return "response" in response.json()


if __name__ == "__main__":
    load_dotenv()
    token = os.environ['VK_ACCESS_TOKEN']
    try:
        link = input("Введите ссылку: ")
        if is_shorten_link(link):
            click_num = count_clicks(token, link)
            print(f"Просмотрела: {click_num} человека")
        else:
            shorted_link = shorten_link(token, link)
            print(f"Сокращенная ссылка: {shorted_link}")
    except requests.exceptions.HTTPError:
        print("Возникла ошибка при попытке обращения к серверу.")