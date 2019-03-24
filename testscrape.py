from bs4 import BeautifulSoup
from selenium import webdriver
import requests


def scrape(link):
    url = link  # "https://www.sephora.sg/products/sephora-collection-browdefining-set/v/default"
    driver = webdriver.Chrome(
        "D:\Downloads\chromedriver_win32 (1)/chromedriver")

    html_doc = driver.get(url)
    a = driver.page_source

    soup = BeautifulSoup(a, 'html.parser')
    h2 = soup.find("h2", {"class": "h2 product-brand"}).contents
    print(h2[0].string)
    driver.close()
    return h2[0].string
# name = h2[0].string
# print(name)
