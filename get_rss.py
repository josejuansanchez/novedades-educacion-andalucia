# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests


def read_rss():
    url = "http://www.juntadeandalucia.es/educacion/portals/delegate/rss/ced/portalconsejeria/profesorado/-/-/true/OR/_self/ishare_noticefrom/DESC/"

    # Hacemos la petición http
    s = requests.Session()
    response = s.post(url)
    #print(response.text)

    # Parseamos el xml
    xml = BeautifulSoup(response.text, "xml")
    items = xml.find_all("item")

    list_of_news = []
    for item in items:
        #print(item.find("title").text)
        #print(item.find("link").text)
        #print(item.find("dc:date").text)
        #print(item.find("pubDate"))
        new = {
            'title': item.find("title").text,
            'link': item.find("link").text,
            'date': item.find("dc:date").text
            }
        list_of_news.append(new)
    return list_of_news

'''
list = read_rss()
print(list[0]['title'])
print(list[0]['link'])
print(list[0]['date'])
'''
