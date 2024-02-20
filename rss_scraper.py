import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://note.com/igem_ninjas/rss'
req = requests.get(url)
txt = BeautifulSoup(req.text, 'xml')

# CSVファイルのパス
csv_file_path = 'data.csv'

# 既存の記事のURLを格納するセット
existing_urls = set()
# 最後のindexを保持する変数
last_index = -1

# CSVファイルが存在する場合、既存のURLを読み込み、最後のindexを更新
if os.path.exists(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row:
                existing_urls.add(row['url'])
                last_index = int(row['index'])  # 最後のindexを更新

# 新しい記事の情報を追加
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['index', 'title', 'description', 'url']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # ファイルが新しく作成される場合、ヘッダーを追加
    if last_index == -1:
        writer.writeheader()

    # 各記事の情報をCSVに書き込む
    for item in txt.find_all('item'):
        title = item.title.string
        description_html = item.description.string
        description_soup = BeautifulSoup(description_html, 'html.parser')
        description = description_soup.get_text()
        link = item.link.string

        # URLが既に存在している場合は追加しない
        if link not in existing_urls:
            last_index += 1  # 新しいindexを割り当て
            writer.writerow({'index': last_index, 'title': title, 'description': description, 'url': link})
            existing_urls.add(link)  # 追加したURLをセットに追加
