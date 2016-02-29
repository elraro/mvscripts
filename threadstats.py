import requests
import operator
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
from prettytable import PrettyTable
import lxml

thread = input("Thread: ")
type(thread)


def total_posts_count(total_pages, thread):
    r = requests.get(thread + "/" + str(total_pages))
    r.content
    soup = BeautifulSoup(r.content, "lxml")
    post_count = soup.find_all("a", {"class": "qn"})
    return int(post_count[len(post_count)-1].text.replace("#", ""))


r = requests.get(thread)
r.content
soup = BeautifulSoup(r.content, "lxml")
try:
    total_pages = soup.find_all("a", {"class": "last"})[0].text
except:
    total_pages = 1
total_posts = total_posts_count(total_pages, thread)
count = 0
user_list = {}
for i in range(int(total_pages)):
    autors = soup.find_all("dt")
    for autor in autors:
        autor_list = autor.find_all("a")
        for name in autor_list:
            if((name.text in user_list) == False):
                user_list[name.text] = 1
            else:
                posts = user_list[name.text]
                user_list[name.text] = posts + 1
    if (i != total_pages):
        if (i == 0):
            r = requests.get(thread+"/"+str(i+2))
            r.content
            soup = BeautifulSoup(r.content)
        else:
            r = requests.get(thread+"/"+str(i+1))
            r.content
            soup = BeautifulSoup(r.content)

total = 0
cont = 0
table = PrettyTable(["User", "Posts"])
table.align["User"] = "l"
table.padding_width = 1

for key, value in sorted(
                        user_list.items(), key=operator.itemgetter(1),
                        reverse=True):
    cont = cont + 1
    total = total + value
    table.add_row([key, value])
print (table.get_string(start=0, end=5))
table = PrettyTable(["Total posts", "Visible Posts", "Hidden Posts",
                    "% Visible", "% Hidden"])
table.padding_width = 1
table.add_row([total_posts, total, total_posts - total, (total * 100) /
              total_posts, ((total_posts - total)*100 / total_posts)])
print (table)
