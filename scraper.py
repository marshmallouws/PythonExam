import bs4
import requests
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# from selenium.webdriver.firefox.options import Options


def search(song_info):
    url = "https://www.genius.com"

    options = Options()
    options.headless = True
    # op = webdriver.FirefoxOptions()
    # op.add_argument("headless")

    browser = webdriver.Firefox(options=options)
    browser.get(url)
    browser.implicitly_wait(3)
    query = song_info['song_name'] + " " + song_info['artist_name']

    # op = webdriver.ChromeOptions()
    # op.add_argument('headless')
    # driver = webdriver.Chrome(options=op)

    search_field = browser.find_element_by_name("q")
    search_field.clear()
    search_field.send_keys(query + Keys.RETURN)
    browser.implicitly_wait(5)
    a = browser.find_elements_by_class_name("mini_card-thumbnail")
    print(a)
    a[0].click()

    # link = browser.find_element_by_css_selector("[href^=#about]")
    # link = browser.find_element_by_xpath('//a[@href="#about"]')
    # print("--------------------------", link)
    # browser.implicitly_wait(3)
    # link.click()
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

    # print(result)

    arr = result.split("\n")
    print(arr[0])
    return arr[0]


#search("blank space", "taylor swift")

def search2(song_info):
    artist = re.sub(
        r"\(.*\)", "", song_info['artist_name'].replace("'", "")).strip().replace(" ", "-")
    song = re.sub(
        r"\(.*\)", "", song_info['song_name'].replace("'", "")).strip().replace(" ", "-")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(
        "https://www.songfacts.com/facts/"+artist+"/"+song, headers=headers)
    print(response.status_code)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    comment = soup.find("ul", {"class": "songfacts-results"})
    result = "We couldn't find much buzz about this song :(" if comment is None else comment.getText(
    )
    return result
