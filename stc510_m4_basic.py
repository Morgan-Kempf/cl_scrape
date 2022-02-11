import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

keywords = ['mattress', 'cabinet', 'wrench']
filename = 'craigslist.csv'
url = 'https://phoenix.craigslist.org/search/gms'


def grabpost(thisurl):
    thispage = requests.get(thisurl)
    bs = BeautifulSoup(thispage.text,'html.parser')
    post_body = bs.find(id='postingbody')
    
    if post_body.text:
        post_text = post_body.text
        for word in keywords:
            if word in post_text:
                title = bs.find(id='titletextonly').text
                time_posted = bs.find('time').text.strip()
                address = bs.find(class_='mapaddress').text
            
                return {'url':thisurl, 'title': title, 'time': time_posted,
                       'address': address, 'post_text': post_text}

def findposts(mainurl):
        df = pd.read_csv(filename)
        mainpage = requests.get(mainurl)
        main_bs = BeautifulSoup(mainpage.text,'html.parser')
        links = main_bs.find_all(class_='result-title hdrlnk')
        for eachlink in links:
            full_url = eachlink['href']
            if not df.url.str.contains(full_url).any():
                print('getting',full_url)
                post = grabpost(full_url)
                sleep(15)
                df = df.append(post,ignore_index=True)
        df.to_csv(filename)
    
findposts(url)
