import utility
import time
import logging
import telebot
from logging.handlers import RotatingFileHandler

bot = telebot.TeleBot("TOKEN")


def main():
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    handler = RotatingFileHandler(filename='dealsnotify.log', maxBytes=1048576,
                                  backupCount=5)
    fmt = logging.Formatter(FORMAT)
    handler.setFormatter(fmt)
    logging.getLogger('').addHandler(handler)
    logging.info('Started')
    # utility.get_threads("ofertas")
    utility.scan_first_page("ofertas", bot)
    logging.info('Finished')

if __name__ == '__main__':
    main()
