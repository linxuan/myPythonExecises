# coding=utf-8
import csv
import re

import requests
from fake_useragent import UserAgent


def get_info(url):
    global UA, HEADER, FILENAME
    response = requests.get(url, headers=HEADER)
    content = response.text
    regex = re.compile(r'<div class="item">.*?<em class="">(?P<rank>.*?)</em>'
                       r'.*?<div class="info">.*?<span class="title">(?P<movie_name>.*?)</span>'
                       r'.*?<div class="bd">.*?导演:(?P<Director>.*?)&nbsp'
                       r'.*?<br>(?P<year>.*?)&nbsp'
                       r'.*?&nbsp;(?P<Region>.*?)&nbsp'
                       r'.*?average">(?P<score>.*?)</span>', re.S)
    it = regex.finditer(content)
    with open(FILENAME, 'a+', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        for _ in it:
            dic = _.groupdict()
            dic['year'] = dic['year'].strip()
            w.writerow(dic.values())
    f.close()


UA = UserAgent()
HEADER = {
    "user-agent": UA.random
}
FILENAME = 'doubanTop250.csv'

with open(FILENAME, 'w', newline='', encoding='gbk') as f:
    w = csv.writer(f)
    w.writerow(['Rank', 'Movie', 'Director', 'Year', 'Region', 'Score'])
f.close()

for i in [0, 25, 50, 75, 100, 125, 150, 175, 200, 225]:
    url = f'https://movie.douban.com/top250?start={i}'
    get_info(url)

