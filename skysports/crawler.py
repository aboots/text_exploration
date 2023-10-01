import json
import os
import time

import requests
from bs4 import BeautifulSoup

DIRNAME = 'skysports'
os.makedirs(DIRNAME, exist_ok=True)

sports = {
    'football': 'sdc-article-body sdc-article-body--lead',
    'f1': 'article__body article__body--lead callfn',
    'cricket': 'article__body article__body--lead callfn',
    'golf': 'article__body article__body--lead callfn',
    'nfl': 'article__body article__body--lead callfn',
    'darts': 'article__body article__body--lead callfn',
}
data = {}
pages = 15

for sport in sports.keys():
    print(sport)
    data[sport] = {}
    for i in range(pages):
        print(i)
        base_url = f'https://www.skysports.com/{sport}/news/more/{i + 1}'
        f = requests.get(base_url)
        soup = BeautifulSoup(f.content, 'lxml')
        news_list = []
        for item in soup.findAll('a', {'class': 'news-list__headline-link'}):
            news_list.append(item['href'])
        for url in news_list:
            if '/news/' not in url:
                continue
            title = url.split('/')[-1]
            f = requests.get(url)
            soup = BeautifulSoup(f.content, 'lxml')
            try:
                paragraphs = soup.findAll('div', {'class': sports[sport]})[0].findAll('p')
            except Exception as e:
                print('can not parse')
                print(url)
                continue
            text = " ".join(p.text for p in paragraphs)
            if title in data[sport]:
                print('repeated news')
                print(url)
                continue
            data[sport][title] = text

    print("Start sleeping for security blocking reasons for 10 seconds.")
    time.sleep(10)
    print("Waken up.")

with open(f"{DIRNAME}/data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)
