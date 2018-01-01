#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import json
import logging
import threading

from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from database import DataBase
from filehandler import FileHandler
from rss import RSS


class EducaBot(object):

    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Create a file handler and read the configuration file
        self.filehandler = FileHandler()
        self.config = self.filehandler.load_json('config.json')

        # Create a database instance
        self.database = DataBase(self.config['database_path'])

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(self.config['bot_token'])

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("stop", self.stop))
        self.dp.add_handler(CommandHandler("help", self.help))
        self.dp.add_handler(CommandHandler("today", self.today))
        self.dp.add_handler(CommandHandler("last", self.last))
        self.dp.add_handler(CommandHandler("all", self.all))

        # log all errors
        self.dp.add_error_handler(self.error)

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

if __name__ == '__main__':
    EducaBot()
