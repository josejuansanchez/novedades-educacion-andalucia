#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import logging
import threading
from datetime import datetime

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

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

        # Create the Application and pass it your bot's token.
        self.application = Application.builder().token(self.config['bot_token']).build()

        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("today", self.today))
        self.application.add_handler(CommandHandler("last", self.last))
        self.application.add_handler(CommandHandler("all", self.all))

        # Register the error handler
        self.application.add_error_handler(self.error_handler)

        # Parse RSS
        self.parse_rss()

        # Send today news to users
        self.send_today_news_to_users()

        # Start the Bot until the user presses Ctrl-C
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        self.database.add_user(user)
        text = '¡Suscripción realizada correctamente!'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        self.database.delete_user(user.id)
        text = 'Suscripción cancelada'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = 'Help!'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        #self.logger.warn('Update "%s" caused error "%s"' % (update, error))
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)

    async def today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        news = self.database.get_today_news()

        if (len(news) <= 0):
            text = 'Sin novedades'
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

            return

        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    async def last(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        news = self.database.get_last_news()
        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    async def all(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        news = self.database.get_all_news()
        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

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

if __name__ == '__main__':
    EducaBot('config/config.json')
