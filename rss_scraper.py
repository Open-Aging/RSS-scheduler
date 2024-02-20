import requests
from bs4 import BeautifulSoup
import csv
import os
import json

webhook_url = 'https://discord.com/api/webhooks/1209480639167070218/7D-ktxpEgCH1UA7C1jcUcs1bQuyNQWZUvQofdDt2dhN6NZn6Es8C5WoRj5BxOzOM8NWD'
headers = {
    'Content-Type': 'application/json'
}

# rss_url = 'https://note.com/igem_ninjas/rss'
# rss_url = 'https://escholarship.org/rss/unit/iha'
rss_url = 'https://news.mit.edu/topic/mitaging-rss.xml'

req = requests.get(rss_url)
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
    post_articles = []
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

            post_articles.append([last_index, link])

    formatted_data = [f'{item[0]}' + ', ' + f'{item[1]}' for item in post_articles]

    formatted_data_splited = [formatted_data[i:i + 5] for i in range(0, len(formatted_data), 5)]
    for i in range(len(formatted_data_splited)):
        message_content = '\n \n'.join(formatted_data_splited[i]) + '\n \n https://chat.openai.com/g/g-kN03aPU6N-aging-insights-assistant'

        print(message_content)
        data = {
            "content": message_content
        }

        print(data)
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        if response.status_code == 204:
            print("Success!")
        else:
            print(f"Failed to post data. Status code: {response.status_code}")
