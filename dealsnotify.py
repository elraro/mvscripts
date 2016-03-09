import utility
import time
import logging
import telebot


bot = telebot.TeleBot("TOKEN")


def main():
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='dealsnotify.log',
                        level=logging.INFO, format=FORMAT)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.info('Started')
    # utility.get_threads("ofertas")
    utility.scan_first_page("ofertas", bot)
    logging.info('Finished')

if __name__ == '__main__':
    main()
