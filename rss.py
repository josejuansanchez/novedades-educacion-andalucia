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

    list_of_news = []
    for item in items:
        new = {
            'title': item.find("title").text,
            'link': item.find("link").text,
            'date': item.find("dc:date").text
            }
        list_of_news.append(new)
    return list_of_news

def save_news_in_db(list):
    db = sqlite3.connect('data/novedades.sqlite')
    cursor = db.cursor()

    for item in list:
        title = item['title']
        link = item['link']
        date = item['date']
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

    list_of_news = []
    for row in rows:
        new = {
            'title_and_link': row[1] + '\n\n' + row[2]
            #'title': row[1],
            #'link': row[2],
            #'date': row[3]
            }
        list_of_news.append(new)

    db.close()
    return list_of_news

def get_last_news():
    query = "SELECT * FROM news WHERE date >= date('now')"
    return get_news_from_db(query)

def get_all_news():
    query = "SELECT * FROM news ORDER BY date DESC"
    return get_news_from_db(query)

def main():
    for url in urls:
        news = get_news_from_rss(url)
        save_news_in_db(news)
        #news = get_news_from_db()
        #print(news)

if __name__ == '__main__':
    main()
