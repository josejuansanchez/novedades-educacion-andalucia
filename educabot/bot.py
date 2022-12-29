#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from telegram import Update, InputMediaPhoto
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
        
        # Temporary command
        #self.application.add_handler(CommandHandler("test", self.test))

        # Register the error handler
        self.application.add_error_handler(self.error_handler)

        # Create a job queue
        self.job_queue = self.application.job_queue

        # Create a job to parse RSS
        self.job_queue.run_repeating(self.parse_rss, interval=3600, first=10)

        # Create a job to send today news to users 
        self.job_queue.run_repeating(self.send_today_news_to_users, interval=3600, first=30)
        
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

    async def send_today_news_to_users(self, context: ContextTypes.DEFAULT_TYPE):
        news = self.database.get_today_news()
        users = self.database.get_users_telegram_id()

        for new in news:
            text = '<b>' + new['source_name'] + '</b>\n\n' + new['title'] + '\n\n' + new['link']

            for user in users:
                if not self.database.is_new_received_by_user(new['id'], user['telegram_id']):
                    await context.bot.send_message(chat_id=user['telegram_id'], text=text, parse_mode=ParseMode.HTML)
                    self.database.add_new_received_by_user(new['id'], user['telegram_id'])

    async def parse_rss(self, context: ContextTypes.DEFAULT_TYPE):
        rss = RSS(self.config_file_path)
        for source in rss.config['sources']:
            news = rss.get_news(source)
            rss.save_news_to_db(news)
            print('Source: ' + source['name'] + ' parsed at: ' + str(datetime.now()) + '. ' + str(len(news)) + ' items found')

    # Temporary method
    async def test(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        rss = RSS(self.config_file_path)
        for source in rss.config['sources']:
            news = rss.get_news_from_lavoz(source)  

            for new in news:  
                text = '<b><a href="https://12ft.io/proxy?q=' + new['link'] + '">' + new['title'] + '</a></b>\n\n' + new['description'] + '\n\n' + new['source_name'] + '. ' + new['date']

                media = [
                    InputMediaPhoto(media=new['image'], caption=text, parse_mode=ParseMode.HTML)
                ]

                await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)

if __name__ == '__main__':
    EducaBot('config/config.json')