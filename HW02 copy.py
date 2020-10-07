import csv
from bs4 import BeautifulSoup
import requests
import json
import re
import pprint

# with open('foreign_trade.html') as html_file:
#     soup = BeautifulSoup(html_file, 'lxml')

# def ReadAndCleanCSV(filename):
#     list = []
#     for i in range(0, 10):
#         list.append(i)
#     return list

# print(soup.prettify())
# match = soup.title
# match = soup.title.text
# match = soup.div
# match = soup.find('div', class_='foot_bottom')

# foot_col = soup.find_all('div', class_='foot_col')

# for foot_col in soup.find_all('div', class_='foot_col'):
#     headline = foot_col.ul.li.text
#     print(headline)

#     print()

# print(foot_col)

source = requests.get('http://coreyms.com').text

soup = BeautifulSoup(source, 'lxml')

# Create and reand csv file
csv_file = open('cms_scrap.csv', 'w')
# Write on csv_file
csv_writer = csv.writer(csv_file)
# Write headers on csv_file
csv_writer.writerow(['headline', 'summary', 'vide_link'])

# print(soup.prettify())

article = soup.find('article')
# print(article.prettify())
for article in soup.find_all('article'):

    print()

    headline = article.h2.a.text
    print(headline)
    print()

    summary = article.find('div', class_='entry-content').p.text
    print(summary)
    print()


    try:
        # vid_source = article.find('iframe', class_='youtube-player')
        vid_source = article.find('iframe', class_='youtube-player')['src']
        # print(vid_source)

        # vid_id = vid_source.split('/')
        vid_id = vid_source.split('/')[4]   #index 4

        # vid_id = vid_id.split('?')  #get id
        vid_id = vid_id.split('?')[0]   #index 0 = id
        # print(vid_id)

        # Youtube link
        yt_link = f'https://youtube.com/watch?v={vid_id}'

    except Exception as e:
        # raise e
        # pass
        yt_link = None
    
    print(yt_link)
    print()
    print('=====================================')

    csv_writer.writerow([headline, summary, yt_link])

csv_file.close()