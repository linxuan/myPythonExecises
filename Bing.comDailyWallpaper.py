# coding=utf-8
import os

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm

# 基本参数设置
url = 'https://www.todaybing.com'
ua = UserAgent()
header = {
    "user-agent": ua.random
}
print('*' * 50)
print('Bing.com Daily Wallpaper Downloader for win V1.0\nAuthor: linxuan')
print('*' * 50)

# 获取图片下载地址
res = requests.get(url, headers=header, stream=True)
soup = BeautifulSoup(res.text, 'html.parser')
image_url_tag = soup.find_all(name='a', attrs={'class': 'text-white btn btn-sm btn-primary'})
for _ in image_url_tag:
    image_link = _.get('href')

# 获取图片名称
image_name_tag = soup.find(name='span', attrs={"data-action": "user_like"})
image_name = image_name_tag.get('data-id')
detail_page_url = f'https://www.todaybing.com/detail/{image_name}.html'
detail_res = requests.get(detail_page_url, headers=header)
detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
filename_tag = detail_soup.find_all(name='h2', attrs={'class': 'mb-3 meta-title'})
for _ in filename_tag:
    filename = _.text

# 下载图片
filename += '.jpg'
if not os.path.exists('BingDailyWallpaper'):
    os.mkdir('BingDailyWallpaper')
    os.chdir('BingDailyWallpaper')
else:
    os.chdir('BingDailyWallpaper')
if not os.path.exists(filename):
    download_res = requests.get(image_link, headers=header, stream=True)
    content_size = int(download_res.headers.get('content-length', 0))
    with open(filename, 'wb') as f:
        for data in tqdm(iterable=download_res.iter_content(1024), total=content_size, unit='k',
                         desc=f'Downloading {filename} '):
            f.write(data)
    f.close()
    print('Download Complete. The image is saved in .\\BingDailyWallpaper\\')
elif os.path.exists(filename):
    print(f'{filename} is already downloaded.')
