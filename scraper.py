import bs4
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def search(song_info):
    url = "https://www.genius.com"

    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options)
    browser.get(url)
    browser.implicitly_wait(3)
    query = song_info["song_name"] + " " + song_info["artist_name"]

    search_field = browser.find_element_by_name("q")
    search_field.clear()
    search_field.send_keys(query + Keys.RETURN)
    browser.implicitly_wait(5)
    a = browser.find_elements_by_class_name("mini_card-thumbnail")
    print(a)
    a[0].click()

    browser.implicitly_wait(3)

    response = requests.get(browser.current_url)
    print(response.status_code)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    comment = soup.find("div", {"class": "ikywhQ"})  # about box
    result = (
        "We couldn't find much buzz about this song :("
        if comment is None
        else re.sub(r"^https?:\/\/.*[\r\n]*", "", comment.getText(), flags=re.MULTILINE)
    )

    browser.close()
    arr = result.split("\n")
    print(arr[0])
    return arr[0]


def search2(song_info):
    artist = (
        re.sub(r"\(.*\)", "", song_info["artist_name"].replace("'", ""))
        .strip()
        .replace(" ", "-")
        .replace(".", "")
    )
    song = (
        re.sub(r"\(.*\)||(\ \-\ .*)", "", song_info["song_name"].replace("'", ""))
        .strip()
        .replace(" ", "-")
        .replace(".", "")
    )

    headers = {"User-Agent": "Googlebot/2.1"}
    response = requests.get(
        "https://www.songfacts.com/facts/" + artist + "/" + song, headers=headers
    )
    print(response.status_code)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    comment = soup.find("ul", {"class": "songfacts-results"})
    comment = comment.find("li") if comment is not None else None
    result = (
        "We couldn't find much buzz about this song :("
        if comment is None
        else comment.getText()
    )
    return result
