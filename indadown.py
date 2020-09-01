import threading
from threading import Thread
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.firefox.options import Options

import urllib.request
import winsound
import selenium.webdriver as webdriver
import urllib.request

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
#driver.set_window_position(-10000,0)

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def getHtml(url):
    htmlSource = ""
    with urllib.request.urlopen(url) as f:
        try:
            htmlSource = f.read()
        except ConnectionResetError:
            print("Error with the connection...")
            winsound.Beep(760, 100)
    
    return htmlSource

def getEmbed(html):
    soup = BeautifulSoup(html, 'html.parser')
    iframe = soup.findAll("iframe")[0]
    embed = "https:"+ iframe["src"]
        
    return embed

def getVideoLink(embed):
    driver.get(embed)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    videoLink = soup.find_all("video")[1]["src"]
   
    
    return videoLink

def getEpisode(before):
    episode = ""
    for c in before[::-1]:
        if c.isnumeric():
            episode += c
    
    return episode[::-1]

def splitUpUrl(url):
    before = ""
    after = ""
    episode = ""
    tag = ""
    
    if "resz" in url:
        before = url.split("resz")[0]
        after = url.split("resz")[1]
        episode = getEpisode(before)
        tag  = "resz"
    
    return before, after, episode, tag

def downloadVideo(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=output_path.split(".")[0]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def changeEpisode(before, nextEpisode):
    nextEpisode = list(nextEpisode)[::-1]
    for i in range(len(before)):
        if before[i].isnumeric():
            listed = list(before)
            listed[i] = nextEpisode.pop()
            before = "".join(listed)
    
    return before

def downloadVideos(url, count):
    for c in range(count):
        before, after, episode, tag = splitUpUrl(url)
        episode = int(episode) + c
        
        url = changeEpisode(before, str(episode)) + tag + after
        print("URL: " + url)
        html = getHtml(url)
        
        embed = getEmbed(html)
        print("Getting video link...")
        videoLink = getVideoLink(embed)
        
        downloadVideo(videoLink, str(episode) + ".mp4")


def main():
    global driver
    print("")
    url = "https://indavideo.hu/video/Jojos_Bizarre_Adventure_-_16_resz_magyar_felirattal_"
    count = 3
    #startUrl = input("Give me the start url: ")
    #count = input("How many episodes: ")
    downloadVideos(url, count)
    driver.quit()

if __name__ == "__main__":
    main()