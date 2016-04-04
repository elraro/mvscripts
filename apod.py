import utility
import time
import requests
from bs4 import BeautifulSoup

def main():
    browser = utility.login("user", "password")
    data = utility.get_apod()
    title = data['title']
    explanation = data['explanation']
    type = data['media_type']
    message = '[b]{}[/b]\n\n{}\n\n'.format(title,explanation)
    if "image" in type:
        if data['hdurl']:
            message = message + '[img]{}[/img]'.format(data['hdurl'])
        else:
            message = message + '[img]{}[/img]'.format(data['url'])
    else:
        video = data['url'].lstrip('https://www.youtube.com/embed/')
        message = message + '[video]https://www.youtube.com/watch?v={}[/video]'.format(video)
    utility.post(message, 555411, browser)

if __name__ == '__main__':
    main()
