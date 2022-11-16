from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import packaging
import re 

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=s, chrome_options=options)

url = "https://www.youtube.com/watch?v=V-D6eZwMd5g"
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
##raw_like = soup.find('button', {'class': 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'})
#likes = soup.find("span", {"class" : "like-button-renderer"}).text
#thumbs = soup.find("span", {"class": "style-scope yt-formatted-string bold"})
#print("this video has been liked" ,likes,"times")
##print(raw_like["aria-label"])


##.find_all(re.compile("^[1-9](,[1-9])*$"))

##print("----")

## description
pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
description = pattern.findall(str(soup))[0].replace('\n','\n')
print("Description: "+description)
print("----")

## links in Description
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description)
print("Links in description : ", urls, "\n")

driver.quit()