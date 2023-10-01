# requirements: beautifulsoup4==4.7.1 requests==2.22.0 lxml==4.3.4

import json
import os
from collections import Counter

import requests
from bs4 import BeautifulSoup

DIRNAME = 'zoomg-movies-review'

os.makedirs(DIRNAME, exist_ok=True)
texts_dic = {}
writers_counter = Counter()
option = 2
total_pages = 15
for i in range(1, total_pages + 1):
    url = f"https://www.zoomg.ir/movie-tv-show-review/page/{i}/"
    f = requests.get(url)
    soup = BeautifulSoup(f.content, 'lxml')
    movies_links = []
    for link in soup.findAll('a', {'class': 'imgwrapper'}):
        movies_links.append(link['href'])
    for link in movies_links:
        if 'review' not in link.split('/')[-2]:
            continue
        f = requests.get(link)
        final_text = ''
        soup = BeautifulSoup(f.content, 'lxml')
        p_list = soup.findAll('div', {'id': 'bodyContainer'})[0].findAll('p')
        for p in p_list:
            final_text += p.text
        try:
            writer = soup.findAll('div', {'class': "author-details d-flex"})[0].findAll('a')[0].text
            writers_counter.update({writer: 1})
        except Exception as e:
            print(link)
            continue
        texts_dic[' '.join(link.split('/')[-2].split('-')[1:-1])] = {'writer': writer,
                                                                     'text': final_text}
    print(f'{i} page out of {total_pages} done.')
if option == 1:
    for key, value in texts_dic.items():
        with open(f"{DIRNAME}/{key}.txt", "w", encoding="utf-8") as text_file:
            text_file.write(json.dumps(value, ensure_ascii=False))
elif option == 2:
    with open(f"{DIRNAME}/movies.json", "w", encoding="utf-8") as file:
        json.dump(texts_dic, file, ensure_ascii=False)
print(writers_counter.most_common(5))
