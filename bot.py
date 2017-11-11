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

from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from rss import *


# Read configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')

def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def today(bot, update):
    list = get_today_news()

    if (len(list) <= 0):
        update.message.reply_text("Sin novedades")
        return

    for item in list:
        update.message.reply_text(item['title_and_link'], ParseMode.HTML)

def last(bot, update):
    list = get_last_news()
    for item in list:
        update.message.reply_text(item['title_and_link'], ParseMode.HTML)

def all(bot, update):
    list = get_all_news()
    for item in list:
        update.message.reply_text(item['title_and_link'], ParseMode.HTML)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['bot-token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("last", last))
    dp.add_handler(CommandHandler("all", all))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
