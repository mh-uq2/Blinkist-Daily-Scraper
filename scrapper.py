
# coding: utf-8
from bs4 import BeautifulSoup
from datetime import datetime
import tomd
import urllib3

http = urllib3.PoolManager()
urllib3.disable_warnings()

def get_element_from_request(url, element, class_):
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), "html5lib")
    return soup.find(element, class_ = class_)

# Get meta data
# daily = 'https://www.blinkist.com/nc/daily'
# response = http.request('GET', daily)

# soup = BeautifulSoup(response.data.decode('utf-8'), "html5lib")
# container = soup.find('div', class_="dailyV2__free-book__container")
container = get_element_from_request('https://www.blinkist.com/nc/daily', 'div', "dailyV2__free-book__container")

title = container.find('div', 'dailyV2__free-book__title').string.strip()
author = container.find('div', 'dailyV2__free-book__author').string.strip()
cta = container.find('div', 'dailyV2__free-book__cta').a['href']

# Get actual content
# url = f'https://www.blinkist.com{cta}'
# response = http.request('GET', url)

# soup = BeautifulSoup(response.data.decode('utf-8'), "html5lib")
# article = soup.find('article')

article = get_element_from_request(f'https://www.blinkist.com{cta}', 'article', 'shared__reader__blink reader__container__content')
# Convert to markdown and dump to a file
output = tomd.convert(str(article).strip())
date = datetime.now().strftime('%Y%m%d')
with open(f'./books/{date}-{title}-{author}.md', "w") as text_file:
    text_file.write(output)
