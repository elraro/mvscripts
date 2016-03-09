from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import csv
import random
import requests
import logging
import time
import datetime
from tinydb import TinyDB, Query


def login(user, password):
    browser = RoboBrowser(parser="lxml")
    browser.open('http://m.mediavida.com/login.php')
    login = browser.get_form(class_='full')
    login['name'].value = user
    login['password'].value = password
    browser.submit_form(login)
    return browser


def post(message, tid, browser):
    browser.open('http://www.mediavida.com/foro/post.php?tid={}'.format(tid))
    mssg = browser.get_form(class_='single')
    mssg['cuerpo'].value = message
    browser.submit_form(mssg)


def get_news():
    data = []
    url = 'http://www.mediavida.com/foro/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    for ul in soup.find_all('ul', "items small destacados"):
        for li in ul.find_all('li'):
            new = (li.text, 'www.mediavida.com' + str(li.find("a")['href']))
            data.append(new)
    return data


def get_threads(subforum):
    db = TinyDB('db.json')
    table = db.table('dealsbot')
    url = 'https://www.mediavida.com/foro/{}'.format(subforum)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    total_pages = soup.find("strong", "paginas")
    total_pages = int(total_pages.find("a", "last").text)
    for page in range(1, total_pages + 1):
        url = 'https://www.mediavida.com/foro/{}/p{}'.format(subforum, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.find_all('a', 'hb'):
            table.insert({'url': 'https://www.mediavida.com' + a['href']})


def scan_first_page(subforum, bot):
    chat_id = "@mvnews"
    db = TinyDB('db.json')
    table = db.table('dealsbot')
    url = 'https://www.mediavida.com/foro/{}'.format(subforum)
    try:
        r = requests.get(url)
    except:
        logging.info('Connection Error.')
        return
    soup = BeautifulSoup(r.text, "lxml")
    Thread = Query()
    for a in soup.find_all('a', 'hb'):
        href = 'https://www.mediavida.com' + a['href']
        result = table.search(Thread.url == href)
        if not result:
            table.insert({'url': href})
            logging.info('New deal: '+href)
            text = ('[{}]' + '({})').format(a.text, href)
            bot.send_message(chat_id, text, parse_mode='Markdown')


def last_new(table):
    last = table.get(eid=len(table))
    return last['url']


def get_month_text():
    now = datetime.datetime.now()
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
              "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return months[now.month - 1]


def get_year():
    now = datetime.datetime.now()
    return now.year


def new_thread(message, title, category, fid, browser):
    browser.open('http://www.mediavida.com/foro/post.php?fid={}'.format(fid))
    thrd = browser.get_form(class_='single')
    thrd['cuerpo'].value = message
    thrd['cabecera'].value = title
    thrd['tag'].value = "" + str(category)
    browser.submit_form(thrd)


def threads(csv_file):
    result = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)
    del result[0]
    return result


def get_porn(subreddit):
    url = 'https://www.reddit.com/r/{}/.json?limit=100'.format(subreddit)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    url = requests.get(url, params=None, headers=headers)
    data = url.json()
    number = random.randint(1, 100)
    url = data['data']['children'][number]['data']['url']
    res = requests.get(url, params=None, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    if "tumblr.com" in url:
        message = '[spoiler=NSFW][img]{}[/img][/spoiler]'.format(url)
        return message
    if "gfycat.com" in url:
        message = '[spoiler=NSFW][video]{}[/video][/spoiler]'.format(url)
        return message
    if "i.imgur" in url:
        url = url.rstrip('v')
        message = '[spoiler=NSFW][img]{}[/img][/spoiler]'.format(url)
        return message
    else:
        url = 'https://i.' + url.lstrip('http://') + '.jpg'
        message = '[spoiler=NSFW][img]{}[/img][/spoiler]'.format(url)
        return message
