from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import packaging
import re 
import json

N = 2 #n

s=Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=s, chrome_options=options)


def getTitle(soup):
    title = soup.find("meta", {"name" : "title"})["content"]
    return(title)
    #print("Title:", title)
    

def getAuthor(soup): 
    author = soup.find("link", {"itemprop" : "name"})["content"]
    return(author)
    #print("Author:", author)
   

def getLikes(soup):
    raw_like = soup.find('button', {'class': 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'})
    while raw_like==None :
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        raw_like = soup.find('button', {'class': 'yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start'})
    return(raw_like["aria-label"])
    #soup.find("span", {"class" : "like-button-renderer"}).text
    #print(raw_like["aria-label"])

##.find_all(re.compile("^[1-9](,[1-9])*$"))



def getDescription(soup):
    try:
        element = driver.find_element(By.XPATH, "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
        element.click()
    except NoSuchElementException:
        pass
    element = driver.find_element(By.XPATH, "//*[@id=\"expand\"]")
    element.click()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    descDiv = soup.find("yt-formatted-string", {"class": "style-scope ytd-text-inline-expander"})
    if "is-expanded" in descDiv:
        print('ui')
    return(descDiv.text)
    #print(descDiv.text)
    

def getLinks(soup):
    ##for a in descDiv(soup.findall('href'))
    #return(links)
    print("----")
    


def getId_video(soup):
    id = soup.find("meta", {"itemprop" : "videoId"})
    return(id)
    ##print("ID:",id["content"])


def getComs(soup):
    commentaires = []
    element = driver.find_element(By.XPATH, "//*[@id=\"comments\"]")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    while commentsList == []:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentsList = soup.find_all("ytd-comment-thread-renderer", {"class": "style-scope ytd-item-section-renderer"}, limit = N)
    for comment in commentsList:
        commentaires.append(comment.find("yt-formatted-string", {"id": "content-text"}).text)
    return(commentaires)
    ##print(commentaires)


def main():
    
    with open("input.json", 'r') as f:
        inputs = json.load(f)        
        
    file = open("input.json")
    data=json.load(file)
    
    dictionnaryList = {'dictionnary': []}
    
    for id in data['videos_id']:
        driver.get("https://www.youtube.com/watch?v=" + id)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)
               
        title = getTitle(soup)
        author = getAuthor(soup)
        likes = getLikes(soup)
        description = getDescription(soup)
        links = getLinks(soup)
        coms = getComs(soup)
        
        print('###')
        print(title, '\n----')
        print(author, '\n----')
        print(likes, '\n----')
        print(description, '\n----')
        print(links, '¬----')
        print(coms, '\n----')
        print('###')
        
        dictionnary = {
        "title": title,
        "author": author,
        "likes": likes,
        "description": description,
        "coms": coms
        }
        dictionnaryList['dictionnary'].append(dictionnary)
        
    with open("output.json", 'w') as f:
        f.write(json.dumps(dictionnaryList, indent=4))
    
    driver.quit()


if __name__ == "__main__":
    main()


