#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from database import DataBase
from filehandler import FileHandler


class RSS(object):

    def __init__(self, config_file_path):
        self.filehandler = FileHandler()
        self.config = self.filehandler.load_json(config_file_path)
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
