import telebot
import utility
import os
import time
from tinydb import TinyDB, Query


bot = telebot.TeleBot("TOKEN")

def main():
    db = TinyDB('db.json')
    table = db.table('newsbot')
    while True:
        try:
            news = utility.get_news()
        except:
            news = []
        last = utility.last_new(table)
        pos = 0
        for i, (title, url) in enumerate(news):
            if last in url:
                del news[i:]
        if news:
            chat_id = "@mvnews"
            table.insert({'url':str(news[0][1])})
            for n in news:
                text = ('[{}]' + '({})').format(n[0], n[1])
                bot.send_message(chat_id, text, parse_mode='Markdown')
        time.sleep(10)
if __name__ == '__main__':
    main()
