from pymongo import MongoClient
from pprint import pprint
import requests
from lxml import html


url = 'https://news.mail.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; rv:86.0) Gecko/20100101 Firefox/86.0'}

news_list = []

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href")
links = links + dom.xpath("//a[@class='list__text']/@href")

for link in links:
    news = {}
    url = link
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)
    datetime = dom.xpath("//span[contains(@class, 'note__text')]/@datetime")[0]
    name = dom.xpath("//h1/text()")[0]
    source = dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]

    news['source'] = source
    news['name'] = name
    news['url'] = url
    news['datetime'] = datetime

    news_list.append(news)

    client = MongoClient('127.0.0.1', 27017)
    db = client['news_db']
    news_db = db.top_news
    news_db.insert_many(news_list)

    pprint(news_list)
