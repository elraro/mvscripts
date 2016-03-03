import telebot
import utility
import os
import time


bot = telebot.TeleBot("TOKEN")


def start(message):
    chat_id = '@mvnews'
    text = "Noticias de MV en Telegram."
    bot.send_message(chat_id, text)


def main():
    while True:
        news = utility.get_news()
        last = utility.last_new("last_new")
        pos = 0
        for i, (title, url) in enumerate(news):
            if last in url:
                del news[i:]
        if news:
            chat_id = "@mvnews"
            os.remove("last_new")
            with open("last_new", "w") as f:
                f.write(str(news[0][1]))
            for n in news:
                text = ('[{}]' + '({})').format(n[0], n[1])
                bot.send_message(chat_id, text, parse_mode='Markdown')
        time.sleep(10)

if __name__ == '__main__':
    main()
