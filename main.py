import os
from string import Formatter

import requests
from os import path
import glob

index_txt = open("index.txt", "w", encoding="utf-8")

BASE_URL = 'https://www.liveinternet.ru/rating/today.tsv?;page={page}'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

LOADS_PACKAGE_NAME = 'loads'


# if needed
# os.mkdir(LOADS_PACKAGE_NAME)

def get_url_for_page(page: int) -> str:
    return Formatter().format(BASE_URL, page=str(page))


sites_count = 0
i = 0
while sites_count < 100:
    try:
        i += 1
        print('page ' + str(i))
        url = get_url_for_page(i)
        pages_response = requests.get(url, headers=HEADERS)
        urls = list(
            map(lambda item: 'http://' + item.split("\t")[1].replace("/", ""), pages_response.text.split("\n")[1:30]))
    except Exception:
        print("Whooooooooops")
        continue
    try:
        for url in urls:
            page_response = requests.get(url, headers=HEADERS)
            filename = LOADS_PACKAGE_NAME + '/' + str(sites_count) + '.' + url.replace('/', '') + ".html"
            html_file = open(filename, "w", encoding="utf-8")
            html_file.write(page_response.text)
            html_file.close()
            index_txt.write(str(sites_count) + '. ' + url + "\n")
            sites_count += 1
            print('loaded ' + str(sites_count) + ' sites')

    except Exception:
        print("Whoooops")
        continue

index_txt.close()
