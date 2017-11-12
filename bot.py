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
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from rss import *


class ProfeBot(object):

    def __init__(self, filename):
        self.read_configuration_file(filename)

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(config['bot-token'])

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help))
        self.dp.add_handler(CommandHandler("today", self.today))
        self.dp.add_handler(CommandHandler("last", self.last))
        self.dp.add_handler(CommandHandler("all", self.all))

        # log all errors
        self.dp.add_error_handler(self.error)

        # Check if there exist news in the database
        self.check_news_in_database()

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def read_configuration_file(self, filename):
        with open(filename, 'r') as f:
            self.config = json.load(f)

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def start(self, bot, update):
        update.message.reply_text('Hi!')
        telegram_user = update.message.from_user
        print(telegram_user)

    def help(self, bot, update):
        update.message.reply_text('Help!')

    def error(self, bot, update, error):
        self.logger.warn('Update "%s" caused error "%s"' % (update, error))

    def today(self, bot, update):
        list = get_today_news()

        if (len(list) <= 0):
            update.message.reply_text("Sin novedades")
            return

        for item in list:
            update.message.reply_text(item['title_and_link'], ParseMode.HTML)

    def last(self, bot, update):
        list = get_last_news()
        for item in list:
            update.message.reply_text(item['title_and_link'], ParseMode.HTML)

    def all(self, bot, update):
        list = get_all_news()
        for item in list:
            update.message.reply_text(item['title_and_link'], ParseMode.HTML)

    def check_news_in_database(self):
        threading.Timer(3600, self.check_news_in_database).start()

        list = get_today_news()

        for item in list:
            self.dp.bot.send_message(chat_id=config['chat-id'], text=item['title_and_link'], parse_mode=ParseMode.HTML)
            set_new_as_published(item['id'])

if __name__ == '__main__':
    ProfeBot('config.json')