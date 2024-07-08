# import requests
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
# Custom module, see database.py in main folder
import methods.database as database

## Function Definitions

def webquery(URL):
    """Generic function for pulling website html.
    
        Takes URL arg
        returns html in soup form
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        # TO DO: Fix the sleep to be dynamically triggered by a body element loading
        sleep(2)
        soup = BeautifulSoup(page.content(), 'lxml')
        browser.close()
    return soup

def penn_job_update():
    """Analysis function for Penn Workday."""
    URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    soup = webquery(URL)
    
    results = str(soup.ul.find_all("a"))

    # Regex finds job names and links from soup
    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'https://wd1.myworkdaysite.com{x}' for x in rawlinks]
    names = re.findall(r'>(.*?)</a>', results)
 
    # pandas dataframe
    table = pd.DataFrame({
        'names': names,
        'links': links
    })

    database.add_to_jobs(1, table)

def comcast_job_update():
    """Analysis function for Comcast.
            
            Basically identical to Penn
    """
    URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/jobs"
    soup = webquery(URL)
    results = str(soup.ul.find_all("a"))

    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'https://comcast.wd5.myworkdayjobs.com{x}' for x in rawlinks]
    names = re.findall(r'>(.*?)</a>', results)
    table = pd.DataFrame({
        'names': names,
        'links': links
    })

    database.add_to_jobs(2, table)

def brookings_job_update():
    """Analysis function for Brookings"""
    URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
    iframe = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078&in_iframe=1"

    page = requests.get(iframe)

    soup = BeautifulSoup(page.content, 'lxml')
    results = str(soup.find_all("div", {"class": "col-xs-12 title"}))

    links = re.findall(r'href="(.*?)"', results)
    names = re.findall(r'title="[0-9].*? - (.*?)"', results)

    table = pd.DataFrame({
            'names': names,
            'links': links
        })
    
    database.add_to_jobs(3, table)