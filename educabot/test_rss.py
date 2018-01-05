#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from rss import RSS

def main():
    rss = RSS('config/config.json')

    for source in rss.config['sources']:
        news = rss.get_news(source)
        rss.save_news_to_db(news)
        print('Source: ' + source['name'] + ' parsed at: ' + str(datetime.now()) + '. ' + str(len(news)) + ' items found')

if __name__ == '__main__':
    main()
