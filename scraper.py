import bs4
import requests
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


def search(songname, artist):
    url = "https://www.genius.com"
    browser = webdriver.Firefox()
    browser.get(url)
    browser.implicitly_wait(3)
    query = songname + " " + artist

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


search("blank space", "taylor swift")
