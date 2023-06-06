import requests
from bs4 import BeautifulSoup
import os

# URLからHTMLを取得しパースする
page_url = 'URL'
r = requests.get(page_url)
soup = BeautifulSoup(r.text, 'html.parser')

# imgタグを全て取得し、src属性の値を取得、リストに格納
img_tags = soup.find_all('img')
img_urls = [img['src'] for img in img_tags if img.get('src')]

# 画像のダウンロードと保存を行う関数


def download_image(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(r.content)


# 保存先ディレクトリを指定する
save_dir = 'images'  # 適宜変更
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 各画像URLをダウンロードし保存する
for i, url in enumerate(img_urls):
    file_name = f'{i}.jpg'
    file_path = os.path.join(save_dir, file_name)
    download_image(url, file_path)
