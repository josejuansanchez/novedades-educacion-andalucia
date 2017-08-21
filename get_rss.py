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

    # Parseamos el xtml
    xml = BeautifulSoup(response.text, "xml")
    items = xml.find_all("item")

    for item in items:
        print(item.find("title").text)
        print(item.find("link").text)
        print(item.find("dc:date").text)
        #print(item.find("pubDate"))
        print("---")
        #print(item)

read_rss()
