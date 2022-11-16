from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import packaging
import re 
import _json

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=s, chrome_options=options)

url = "https://www.youtube.com/watch?v=LPpqcvIlrhQ"
driver.get(url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

## title
title = soup.find("meta", {"name" : "title"})["content"]
print("###")
print("Title:", title)
print("----")

## author 
author = soup.find("link", {"itemprop" : "name"})["content"]
print("Author:", author)
print("----")

## pocebleu (views pr l'instant)
raw_like = soup.find('button', {'class': 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'})
#soup.find("span", {"class" : "like-button-renderer"}).text
print(raw_like["aria-label"])


##.find_all(re.compile("^[1-9](,[1-9])*$"))

print("----")

## description
element = driver.find_element(By.XPATH, "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
element.click()
element = driver.find_element(By.XPATH, "//*[@id=\"expand\"]")
element.click()
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
descDiv = soup.find("yt-formatted-string", {"class": "style-scope ytd-text-inline-expander"})
if "is-expanded" in descDiv:
    print('ui')
print(descDiv.text)
print("----")

## links in Description
#for a in descDiv(soup.find("href"))
#print("----")

## id video 
id = soup.find("meta", {"itemprop" : "videoId"})
print("ID:",id["content"])
print('###')



driver.quit()