import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://note.com/igem_ninjas/rss'
req = requests.get(url)
txt = BeautifulSoup(req.text, 'xml')

# CSVファイルのパス
csv_file_path = 'data.csv'

# CSVファイルが存在するか確認し、indexを決定する
if os.path.exists(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        last_index = int(rows[-1][0]) if rows else -1  # 最後の一行のindexを取得する．なければ-1
else:
    last_index = -1  # ファイルが存在しないとき

# 新しい記事の情報を追加
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # ファイルが新しく作成される場合，ヘッダーを追加
    if last_index == -1:
        writer.writerow(['index', 'title', 'description', 'url'])

    # 各記事の情報をCSVに書き込む
    for item in txt.find_all('item'):
        last_index += 1  # indexをインクリメント
        title = item.title.string
        # descriptionからHTMLタグを取り除く
        description_html = item.description.string
        description_soup = BeautifulSoup(description_html, 'html.parser')
        description = description_soup.get_text()
        link = item.link.string

        writer.writerow([last_index, title, description, link])
