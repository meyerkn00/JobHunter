# import requests
import re
from time import sleep
from dataclasses import dataclass
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

# Output class

class Company:
    def __init__(self, name):
        self.name = name
        self.joblist = []
    
    def add_job(self, joblist):
        self.joblist.append(joblist)
    
    def bundle(self, joblist):
        # for each Job, take results and put into text output for email
        pass

@dataclass
class Job:
    title: str
    link: str
    # location: str

# Penn Demo using playwright

URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL)
    # TO DO: Fix the sleep to be dynamically triggered by a body element loading
    sleep(2)
    soup = BeautifulSoup(page.content(), 'lxml')
    browser.close()

results = str(soup.ul.find_all("a"))
result_elements = soup.ul.find_all("a")

# Regex finds job names and links from soup
links = re.findall(r'(/en-US.*?)"', results)
names = re.findall(r'>([A-Za-z].*?)<', results)

print(links)
print(names)
    
# print([re.sub('<>', "", x) for x in names])
# print([re.sub('/"', "", x) for x in links])