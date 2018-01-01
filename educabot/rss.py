# -*- coding: utf-8 -*-

import json
import sqlite3
import sys
import threading
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database import DataBase
from filehandler import FileHandler


class RSS(object):

    def __init__(self):
        self.filehandler = FileHandler()
        self.config = self.filehandler.load_json('config.json')
        self.database = DataBase(self.config['database_path'])

    def get_news(self, source):
        s = requests.Session()
        response = s.post(source['url'])
        #print(response.text)

        xml = BeautifulSoup(response.text, "xml")
        items = xml.find_all("item")

        news = []
        for item in items:
            new = {
                'title': item.find("title").text,
                'link': item.find("link").text,
                'date': item.find("dc:date").text,
                'source_name': source['name']
            }
            news.append(new)
        return news

    def save_news_to_db(self, news):
        self.database.add_news(news)


def main():

    threading.Timer(3600, main).start()

    rss = RSS()

    for source in rss.config['sources']:
        news = rss.get_news(source)
        rss.save_news_to_db(news)
        print('Source: ' + source['name'] + ' parsed at: ' + str(datetime.now()) + '. ' + str(len(news)) + ' items found')

if __name__ == '__main__':
    main()
