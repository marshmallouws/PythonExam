import bs4
import requests
import re


class Scraper:

    def __init__(self):
        self.formattedSongName = None

    # previous method.
    '''def SetSearch(self, songname, artist):
        self.formattedSongName = (artist + "%20" + songname).replace(" ", "%20").lower()
        return self.formattedSongName'''

    # previous method.
    '''def GetSearchLinks(self):
        response = requests.get("https://genius.com/search?q=" + self.formattedSongName)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        links = soup.find_all('a')

        return links'''

    def SetSearch(self, songname, artist):
        self.formattedSongName = (
            artist + "-" + songname + "-lyrics").replace(" ", "-").lower()
        return self.formattedSongName

    def GetTopComment(self):
        response = requests.get("https://genius.com/" + self.formattedSongName)
        soup = bs4.BeautifulSoup(response.content, "html.parser")

        #stuff = soup.find_all('p')
        stuff = soup.find_all("div", {"class": "hwxsoX"})

        print(stuff)

        #r = re.compile('<div>(.+?)</div>')
        # print(r.findall(response.text))

        return soup
