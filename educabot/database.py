#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3

from filehandler import FileHandler

class DataBase(object):

    def __init__(self, database_path):
        self.database_path = database_path
        self.database_schema = "database/schema.sql"
        self.filehandler = FileHandler()
        self.create_database()

    def create_database(self):
        if not self.filehandler.exists(self.database_path):
            sql_script = self.filehandler.load_file(self.database_schema)
            db = sqlite3.connect(self.database_path)
            cursor = db.cursor()
            cursor.executescript(sql_script)
            db.commit()
            db.close()

    def add_news(self, news):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()

        for new in news:
            title = new['title']
            link = new['link']
            date = new['date']
            source_name = new['source_name']
            cursor.execute(
                '''INSERT INTO news (title, link, date, source_name)
                SELECT ?, ?, ?, ?
                WHERE NOT EXISTS (SELECT 1
                FROM news
                WHERE date = ?)''', (title, link, date, source_name, date))

        db.commit()
        db.close()

    def get_news(self, query):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        news = []
        for row in rows:
            new = {
                'id': row[0],
                'title': row[1],
                'link': row[2],
                'date': row[3],
                'source_name': row[4]
            }
            news.append(new)

        db.close()
        return news

    def get_today_news(self):
        query = "SELECT * FROM news WHERE date >= date('now')"
        return self.get_news(query)

    def get_last_news(self):
        query = "SELECT * FROM news ORDER BY date DESC LIMIT 10"
        return self.get_news(query)

    def get_all_news(self):
        query = "SELECT * FROM news ORDER BY id ASC"
        return self.get_news(query)

    def get_users(self, query):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'telegram_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'language_code': row[4],
                'is_bot': row[5]
            }
            users.append(user)

        db.close()
        return users

    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.get_users(query)

    def get_users_telegram_id(self):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute("SELECT telegram_id FROM users")
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'telegram_id': row[0],
            }
            users.append(user)

        db.close()
        return users

    def add_user(self, user):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()        
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?,?)",
                       (user.id, user.username, user.first_name, user.last_name, user.language_code, user.is_bot))
        db.commit()
        db.close()

    def delete_user(self, id):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE telegram_id = ?", (id,))
        db.commit()
        db.close()

    def is_new_received_by_user(self, new_id, user_id):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM news_received_by_user WHERE telegram_id = ? AND new_id = ?", (user_id, new_id))
        rows = cursor.fetchall()
        db.commit()
        db.close()
        return len(rows)

    def add_new_received_by_user(self, new_id, user_id):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()        
        cursor.execute("INSERT OR IGNORE INTO news_received_by_user VALUES (?,?)", (user_id, new_id))
        db.commit()
        db.close()

    def get_receives(self, query):
        db = sqlite3.connect(self.database_path)
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'telegram_id': row[0],
                'new_id': row[1]
            }
            users.append(user)

        db.close()
        return users

    def get_all_news_received_by_user(self):
        query = "SELECT * FROM news_received_by_user"
        return self.get_receives(query)
