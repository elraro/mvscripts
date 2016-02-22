from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import csv
import random
import requests

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
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    url = requests.get(url, params=None, headers=headers)
    data = url.json()
    number = random.randint(1,100)
    url = data['data']['children'][number]['data']['url']
    res = requests.get(url, params=None, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

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
