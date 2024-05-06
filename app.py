import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Brookings seems to have all of the job search data hidden within javascript. Skipping for now
# URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
# page = requests.get(URL)

# Penn Demo using requests
# URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
# page = requests.get(URL)
# soup = BeautifulSoup(page.content, 'lxml')
# results = soup.find("ul")

#print(soup)

# Penn Demo using playwright

URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)
    sleep(2)
    soup = BeautifulSoup(page.content(), 'lxml')
    browser.close()

results = soup.find("ul")
print(results)