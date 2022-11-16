from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import packaging

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=s, chrome_options=options)

url = "https://www.youtube.com/watch?v=lDOswsnwYPk"
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

## title
title = soup.find("meta", {"name" : "title"})["content"]
print("----")
print("The title is", title)
print("----")

## author 
author = soup.find("link", {"itemprop" : "name"})["content"]
print("The author is", author)
print("----")

## pocebleu (views pr l'instant)
#likes = soup.find("span", {"class" : "like-button-renderer"}).text
#thumbs = soup.find("span", {"class": "style-scope yt-formatted-string bold"})
#print("this video has been liked" ,likes,"times")
#print("----")

## description
description = soup.find("div", {"id" : "snippet"}).text
print(description)
print("----")


driver.quit()