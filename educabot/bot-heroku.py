#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import logging
import os
import threading
from datetime import datetime

from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from database import DataBase
from filehandler import FileHandler
from rss import RSS


class EducaBot(object):

    def __init__(self, config_file_path):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Configuration file path
        self.config_file_path = config_file_path

        # Create a file handler and read the configuration file
        self.filehandler = FileHandler()
        self.config = self.filehandler.load_json(self.config_file_path)

        # Create a database instance
        self.database = DataBase(self.config['database_path'])

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(os.environ['BOT_TOKEN'])

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("stop", self.stop))
        self.dp.add_handler(CommandHandler("help", self.help))
        self.dp.add_handler(CommandHandler("today", self.today))
        self.dp.add_handler(CommandHandler("last", self.last))
        self.dp.add_handler(CommandHandler("all", self.all))

        # Temporary
        self.dp.add_handler(CommandHandler("users", self.users))
        self.dp.add_handler(CommandHandler("news", self.news))
        self.dp.add_handler(CommandHandler("receives", self.receives))

        # log all errors
        self.dp.add_error_handler(self.error)

        # Parse RSS
        self.parse_rss()

        # Send today news to users
        self.send_today_news_to_users()

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def start(self, bot, update):
        user = update.message.from_user
        self.database.add_user(user)
        update.message.reply_text('¡Suscripción realizada correctamente!')

    def stop(self, bot, update):
        user = update.message.from_user
        self.database.delete_user(user.id)
        update.message.reply_text('Suscripción cancelada')

    def help(self, bot, update):
        update.message.reply_text('Help!')

    def error(self, bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))

    def today(self, bot, update):
        news = self.database.get_today_news()

        if (len(news) <= 0):
            update.message.reply_text("Sin novedades")
            return

        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            update.message.reply_text(text, ParseMode.HTML)

    def last(self, bot, update):
        news = self.database.get_last_news()
        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            update.message.reply_text(text, ParseMode.HTML)

    def all(self, bot, update):
        news = self.database.get_all_news()
        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            update.message.reply_text(text, ParseMode.HTML)

    def send_today_news_to_users(self):
        threading.Timer(3600, self.send_today_news_to_users).start()
        news = self.database.get_today_news()
        users = self.database.get_users_telegram_id()

        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']

            for user in users:
                if not self.database.is_new_received_by_user(new['id'], user['telegram_id']):
                    self.dp.bot.send_message(chat_id=user['telegram_id'], text=text, parse_mode=ParseMode.HTML)
                    self.database.add_new_received_by_user(new['id'], user['telegram_id'])

    def parse_rss(self):
        threading.Timer(3600, self.parse_rss).start()
        rss = RSS(self.config_file_path)
        for source in rss.config['sources']:
            news = rss.get_news(source)
            rss.save_news_to_db(news)
            print('Source: ' + source['name'] + ' parsed at: ' + str(datetime.now()) + '. ' + str(len(news)) + ' items found')

    # Temporary
    def users(self, bot, update):
        users = self.database.get_all_users()
        for user in users:
            text = '<b>' + str(user['telegram_id']) + '</b>\n\n' + user['username'] + '\n\n' + user['first_name']
            update.message.reply_text(text, ParseMode.HTML)

    def news(self, bot, update):
        news = self.database.get_all_news()
        for new in news:
            text = '<b>' + str(new['id']) + '</b>\n\n' + new['title'] + '\n\n' + new['date']
            update.message.reply_text(text, ParseMode.HTML)

    def receives(self, bot, update):
        receives = self.database.get_all_receives()
        for receive in receives:
            text = '<b>' + str(receive['telegram_id']) + '</b>\n\n' + str(receive['new_id'])
            update.message.reply_text(text, ParseMode.HTML)

if __name__ == '__main__':
    EducaBot('config/config.heroku.json')
