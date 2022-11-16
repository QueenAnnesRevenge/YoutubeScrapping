from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import time


res = requests.get("https://www.youtube.com/watch?v=fPgW_EH5ASw", timeout=9)
print("Status Code =", res.status_code)

time.sleep(2)
soup = BeautifulSoup(res.text, 'html.parser')

## title
title = soup.find("meta", {"name" : "title"})["content"]
print(title)

## author
author = soup.find("link", {"itemprop" : "name"})["content"]
print(author)

## pocebleuh
thumbs = soup.find("div", {"id": "segmented-like-button"})
print(thumbs)

## description


## links


## video id

## n first comms (if exist)