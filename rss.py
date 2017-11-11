# -*- coding: utf-8 -*-
import sqlite3
import sys

import requests
from bs4 import BeautifulSoup

urls = [
    # Profesorado
    "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/profesorado/-/-/true/OR/_self/ishare_noticefrom/DESC/",

    # Centros
    "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/centro-1/-/-/true/OR/true/cm_modified/DESC/"
]

def get_news_from_rss(url):
    s = requests.Session()
    response = s.post(url)
    #print(response.text)

    xml = BeautifulSoup(response.text, "xml")
    items = xml.find_all("item")

    news = []
    for item in items:
        new = {
            'title': item.find("title").text,
            'link': item.find("link").text,
            'date': item.find("dc:date").text
            }
        news.append(new)
    return news

def save_news_in_db(news):
    db = sqlite3.connect('data/novedades.sqlite')
    cursor = db.cursor()

    for new in news:
        title = new['title']
        link = new['link']
        date = new['date']
        cursor.execute(
            '''INSERT INTO news (title, link, date)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (SELECT 1
            FROM news
            WHERE date = ?)''', (title, link, date, date))

    db.commit()
    db.close()

def get_news_from_db(query):
    db = sqlite3.connect('data/novedades.sqlite')
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    news = []
    for index,row in enumerate(rows):
        new = {
            'title_and_link': '<b>' + str(index + 1) + '</b>. ' + row[1] + '\n\n' + row[2]
            #'title': row[1],
            #'link': row[2],
            #'date': row[3]
            }
        news.append(new)

    db.close()
    return news

def get_today_news():
    query = "SELECT * FROM news WHERE date >= date('now')"
    return get_news_from_db(query)

def get_last_news():
    query = "SELECT * FROM news ORDER BY date DESC LIMIT 10"
    return get_news_from_db(query)

def get_all_news():
    query = "SELECT * FROM news ORDER BY date DESC"
    return get_news_from_db(query)

def main():
    for url in urls:
        news = get_news_from_rss(url)
        save_news_in_db(news)

if __name__ == '__main__':
    main()